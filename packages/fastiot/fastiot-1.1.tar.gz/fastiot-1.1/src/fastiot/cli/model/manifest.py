""" Data model for fastiot service manifests """
import subprocess
from enum import Enum
from tempfile import NamedTemporaryFile
from typing import List, Optional, Dict

import yaml
from pydantic.main import BaseModel

from fastiot.cli.cli_logging import get_cli_logger
from fastiot.cli.constants import DEFAULT_BASE_IMAGE, MANIFEST_FILENAME
from fastiot.util.case_conversions import kebab_case_to_snake_case


class Port(BaseModel):
    """
    A port entry represents one port used by the service which should be mounted outside the container.
    """

    port: int
    """
    The default port location.
    """
    env_variable: str
    """
    The environment variable which is passed to the container to change the port, e.g. for automated testing.
    """


class Volume(BaseModel):
    """
    A volume entry represents one directory used by the service which should be mounted from your host into the
    container.
    """

    location: str
    """
    Provide the location inside the container.
    This value will also be used in your local environment if the defined environment variable is not set.
    """
    env_variable: str
    """
    Define the variable name, that is used to overwrite the default location specified in ``location``. 
    If you put e.g. ``MYSERVICE_DATA_VOLUME`` you may add `something like to following to your :file:`.env` file:
    ``MYSERVICE_DATA_VOLUME=./data`` or ``MYSERVICE_DATA_VOLUME=/opt/myproject/data``.  
    The first one will be used relative to your deployments dir and the docker-compose file in there.
    The second one will be used as absolute path in your filesystem.
    If undefined the path specified in location will also be used on the host.
    If the environment variable is set to an empty string (``""``) the volume will not be mounted and no persistence
    will happen for this volume.
    
    To find the volume inside your service please read the specified environment variable. 
    Inside the container this will be the same as defined in ``location``.
    For debugging purposes the :file:`env` in the build-directory will be adjusted to point to your deployments
    directory.
    """


class Device(BaseModel):
    """
    A device entry represents one device used by the service which should be mounted outside the container.
    """

    location: str
    """
    The default device location, e.g. :file:`/dev/ttyS0` for a serial port
    """
    env_variable: str
    """
    See attribute `env_variable` in :class:`fastiot.cli.model.manifest.Port`.
    """


class MountConfigDirEnum(str, Enum):
    """ Set if the configuration dir needs to be mounted in the container """
    required = "required"  # This will make the config dir available through the docker-compose file.
    optional = "optional"
    no = "no"


class CPUPlatform(str, Enum):
    """ Definition of the CPU platform the container will be built for """

    amd64 = "amd64"  # The most common architecture for servers, desktop and laptop computers with Intel or AMD CPUs.
    amd64_2 = "amd64_2"  # Use more CPU features, s. https://en.wikipedia.org/wiki/X86-64#Microarchitecture_levels
    arm64 = "arm64"  # Modern architecture for e.g. Raspberry Pi 3 and 4 if a 64 Bit OS is used like Ubuntu 20.04
    armv7 = 'armv7'  # 32bit ARM like RasPi with 32 bit OS

    def as_docker_platform(self):
        """ Returns a member (accessed by self in this case!) as docker-style platform. This usually means e.g.
        `linux/amd64`"""
        if self == self.amd64_2:
            return "linux/amd64/2"
        if self == self.armv7:
            return 'linux/arm/v7'
        return "linux/" + self

    def as_qemu_platform(self):
        """ Returns the platform according the qemu emulator """
        if self == self.armv7:
            return 'arm'
        if self == 'amd64_2':
            return 'amd64'
        return self.value


class Healthcheck(BaseModel):
    """
    Configuration options for Docker Healtcheck. This allows for automatic restarting the service if the service
    does not provide the configured life sign.
    """
    cmd: str = ''
    """ Command to run. This could e.g. be a curl request to your API or check wether a logfile gets updated every n
    seconds. """
    interval: str = "30s"
    """ Interval to check the service """
    timeout: str = "30s"
    """ Timeout for the command"""
    start_period: str = "1s"
    retries: int = 3


class NPM(BaseModel):
    """ Use this part if your project contains a frontend created with npm, e.g. a vue.js application """

    src: str  # Source path relative to your application where the code is located
    dist: str = 'dist'
    """
    Destination where npm will place its files for distribution. If not changed npm will have save its files
    in the `<src>/dist` which is also the default here.
    If you have something like::

        service.exports = {
          outputDir:"../flask_server/static",
          assetsDir: "static"
        }


    in your npm config or in case of vue js application in the file :file:`vue.config.js` use the `outputDir` variable
    as relative path here, e.g. ``dist: ../static``
    """
    node_base_image: str = 'node:16-bookworm-slim'
    """
    If you need a different image for building your vue.js app (or whatever) you may define it here.
    The default is currently set to ``node:16-buster-slim``.
    """


class ServiceManifest(BaseModel):
    """
    Every service needs a :file:`manifest.yaml` to describe the service.

    The following options may be used. The file always starts with a ``fastiot_service:`` in the first level. Then
    options from the following may (``name`` must) follow.

    :attr:`fastiot.cli.model.manifest.ServiceManifest.name` is needed, others are mostly optional!
    """
    name: str
    """ Name needs to comply with the services name (Mandatory) """
    ports: List[Port] = []
    """
    Provide a list with some name for the service and a port that this container will open, e.g. when operating
    as a webserver.`
    """
    template: str = 'python3'
    """ Specify the template to use. You can provide your custom Templates by overwriting
    :class:`fastiot.cli.model.docker_template.DockerTemplate`. Make sure that you imported it e.g. via configure.py's
    extensions property. """
    base_image: str = DEFAULT_BASE_IMAGE
    """ Use this to provide an alternative base image, otherwise
    :const:`fastiot.cli.constants.DEFAULT_BASE_IMAGE` will be used.

    Be aware, that the further Dockerfile will be unchanged, thus your base image should be based on some Debian-style.
    If this does not work for you, you may also provide a :file:`Dockerfile` in your service which will automatically be
    used.
    """
    volumes: List[Volume] = []
    """
    Volumes to be mounted in the container
    """
    devices: List[Device] = []
    """
    Devices, e.g. serial devices, to be mounted in the container
    """
    depends_on: List[str] = []
    """
    List of infrastructure services that need to be deployed
    """
    mount_config_dir: MountConfigDirEnum = MountConfigDirEnum.optional
    """
    Specify, if a config dir must be mounted.
    """
    privileged: bool = False
    """
    Enable if this service needs privileged permissions inside docker, e.g. for hardware access
    """
    platforms: List[CPUPlatform] = [CPUPlatform.amd64]
    """ Define the cpu platforms to build the container for. It defaults to amd64. If doing local builds the first one
    specified (or amd64 if none) will be used to build the image. """

    healthcheck: Healthcheck = Healthcheck()
    """
    Configure healthcheck for the container
    """
    copy_dirs_to_container: List[str] = []
    """
    Directories which shall be copied to container. They must be specified relative to :file:`manifest.yaml`.
    """

    npm: Optional[NPM] = None
    """
    If your project contains a vue.js application you can automatically build it here. For required configuration
    see :class:`fastiot.cli.model.manifest.Vue`
    """

    additional_requirements: List[str] = []
    """
    If a specific service needs more packages installed than the others, you may add these here. It will look in the
    requirements directory for the specified additional requirements and copy them inside the container. The 
    :file:`install.sh` must be handle to install these.
    
    Please have a look at :ref:`tut-dependencies` for more information about dependency management in FastIoT.
    """
    compile: bool = True
    """
    If your service  should not be compiled can change to False. Per default your service will be compiled using Nuitka
    to have some obfuscation in the code and potentially speed up the program.
    """
    compose_extras: Optional[Dict] = {}
    """
    **ATTENTION:** Use at your own risk! Adding options not known or duplicating entries in :file:`docker-compose.yaml`
    will make the file invalid and the services will deny to start.
    
    If you want to set some more options for your container, like `mem_limit`, you may list them here.
    You need to know which option accepts docker-compose. Please refer to 
    https://docs.docker.com/compose/compose-file/compose-file-v2/#service-configuration-reference .
    
    For configuring this you can refer to :file:`src/fastiot_sample_services/producer/manifest.yaml`.
    It shows, how you can add more compose extras in manifest.yaml. 
    """

    @staticmethod
    def from_yaml_file(filename: str, check_service_name: str = '') -> "ServiceManifest":
        """ Does the magic of import yaml to pydantic model"""
        with open(filename, 'r') as config_file:
            config = yaml.safe_load(config_file)
            kebab_case_to_snake_case(config)

        manifest = ServiceManifest(**config['fastiot_service'])

        if check_service_name and manifest.name != check_service_name:
            raise ValueError(f'Error raised during parsing of file "{filename}": '
                             f'service name in manifest file "{manifest.name}" differs from expected service '
                             f'name "{check_service_name}".')

        return manifest

    @classmethod
    def from_docker_image(cls, docker_image_name: str, pull_always: bool = False) -> "ServiceManifest":
        # The manifest file is always located inside the container and has the name '/opt/fastiot/manifest.yaml'.
        # We have to mount a volume and copy the file into the volume. If we mounted a file directly, we sometimes get
        # errors overwriting the file from inside the container. To avoid trouble, we mount a directory.

        # Some chars not suitable for docker but for shell commands, do some checking here
        dangerous_chars = [' ', ';', '&', '<', '>', '|']
        if True in [char in dangerous_chars for char in docker_image_name]:
            raise ValueError(f"Image name {docker_image_name} seems to be invalid. Aborting action.")

        pull_str = "--pull always" if pull_always else ""

        export_cmd = f"docker run --rm {pull_str} {docker_image_name} cat /opt/fastiot/{MANIFEST_FILENAME}"
        get_cli_logger().info('Exporting manifest from docker image: %s', docker_image_name)
        get_cli_logger().debug('Using command `%s`', export_cmd)
        with NamedTemporaryFile() as tmp_file:
            ret = subprocess.call(export_cmd.split(), stdout=tmp_file, stderr=subprocess.STDOUT)
            if ret != 0:
                raise OSError(f"Could not read manifest.yaml file from docker image {docker_image_name}")

            # Remove any disturbing docker outputs from the file created from stdout
            tmp_file.seek(0)
            lines = tmp_file.readlines()
            tmp_file.truncate(0)  # Empty file
            tmp_file.seek(0)  # Make sure to start writing at the very beginning of the file
            start_write = False
            for line in lines:
                if not start_write and (line.startswith(b'fastiot_service:') or line.startswith(b'fastiot-service:')):
                    # Now in the cat output and the yaml part
                    start_write = True
                if start_write:
                    tmp_file.write(line)
            tmp_file.seek(0)  # This ensures actual writing

            return cls.from_yaml_file(filename=tmp_file.name)
