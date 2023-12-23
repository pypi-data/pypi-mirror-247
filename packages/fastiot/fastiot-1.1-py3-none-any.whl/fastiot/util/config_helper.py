""" Providing methods to import yaml configuration per service"""

import logging
import os
from typing import Optional, Dict, Union

import yaml
from pydantic import BaseModel

from fastiot.core import FastIoTService
from fastiot.env import env_basic
from fastiot.util.case_conversions import kebab_case_to_snake_case


class FastIoTConfigModel(BaseModel):
    """
    You may use this as a base class to provide a proper data model for your configurations.
    This is a proper alternative to relying on reading in YAML-files and working with dictionaries
    as done with :meth:`fastiot.util.config_helper.read_config`.

    Please consult :ref:`configuration_for_service` for more information about handling configurations and a full
    example.
    """

    @classmethod
    def from_yaml_file(cls, filename: str):
        """ Does the magic of import yaml to pydantic model, provided by a filename."""
        with open(filename, 'r') as config_file:
            config = yaml.safe_load(config_file)
            kebab_case_to_snake_case(config)

        config_object = cls(**config)
        return config_object

    @classmethod
    def from_service(cls, service: Union[FastIoTService, str]):
        """
        Read in the configuration for your service, so just use it with :code:`MyServiceConfig.from_service(self)`
        inside your service.

        It is possible to read the configuration for a service instantiated multiple times.
        If both service.yaml and service_id.yaml exist, service_id.yaml will be preferred.
        Use the environment variable :envvar:`FASTIOT_SERVICE_ID` to set the individual service id for a service.

        Also see :ref:`configuration_for_service` for more information about handling configurations.
        """
        filename = _get_config_file_name(service=service)
        return cls.from_yaml_file(filename=filename)


def _get_config_file_name(service: Union[FastIoTService, str]) -> Optional[str]:
    """
    Find the yaml config file for the given service.

    If both service.yaml and service_id.yaml exist, service_id.yaml will be preferred.

    :param service: service to load the config for (preferred) or name of the config file.
    :return: Filename. May be None if no file was found.
    """

    if isinstance(service, str):
        config_file = os.path.join(env_basic.config_dir, f"{service}")  # Look for file in SAM config
        if os.path.isfile(config_file):
            return config_file
        if (service.startswith("/") or service.startswith(".")) and os.path.isfile(service):
            # An absolute or relative path was provided, so we don’t have to look in the service configuration
            return service

        logging.getLogger("yaml_config").warning("Provided config file %s could not be found.", service)
    else:
        service_name = service.__class__.__name__
        service_id = service.service_id

        config_file_per_service = os.path.join(env_basic.config_dir, f"{service_name}.yaml")
        config_file_per_instance = os.path.join(env_basic.config_dir, f"{service_name}_{service_id}.yaml")

        if os.path.isfile(config_file_per_instance):
            return config_file_per_instance
        if os.path.isfile(config_file_per_service):
            return config_file_per_service

        logging.getLogger("yaml_config").warning("No configuration for service %s was found in %s!",
                                                 service_name, env_basic.config_dir)
    return None


def read_config(service: Union[FastIoTService, str]) -> Dict:
    """
    Load YAML-configuration files based on file (provide string) or, preferably, service.

    It is possible to read the configuration for a service instantiated multiple times.
    If both service.yaml and service_id.yaml exist, service_id.yaml will be preferred.
    Use the environment variable :envvar:`FASTIOT_SERVICE_ID` to set the individual service id for a service.

    Also see :ref:`configuration_for_service` for more information about handling configurations.

    Example passing your service to get a filename configuration automatically:

    >>> from fastiot.core import FastIoTService
    >>> from fastiot.util.config_helper import read_config
    >>>
    >>> class MyService(FastIoTService)
    >>>
    >>>     def __init__(self, **kwargs)
    >>>         super().__init__(**kwargs)
    >>>         my_config = read_config(self)

    :param service: service to load the config for (preferred) or name of the config file.
    :return: Dictionary with the loaded configuration. May be empty if no configuration was found.
    """

    config_file = _get_config_file_name(service)
    if config_file is None:
        return {}

    try:
        with open(config_file) as file:
            result = yaml.safe_load(file)
    except:
        logging.getLogger("yaml_config").warning("Could not open or parse yaml file %s", config_file)
        return {}

    if not result:
        logging.getLogger("yaml_config").warning("Could not parse yaml file %s", config_file)
        return {}
    logging.getLogger("yaml_config").info("Successfully read configuration %s", config_file)
    return result
