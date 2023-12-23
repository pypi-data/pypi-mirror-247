import os

CONFIG_KEY_EXTENSIONS = "extensions"
# Base image used to build docker files if not defined otherwise in the manifest
# Please note that we use buster instead of bullseye because it results in libc-bin segfaults on certain architectures
# sometimes. See also: https://github.com/docker/buildx/issues/314
DEFAULT_BASE_IMAGE = "python:3.11-slim-bookworm"
CONFIGURE_FILE_NAME = "configure.py"
DEPLOYMENTS_CONFIG_DIR = 'deployments'
DEPLOYMENTS_CONFIG_FILE = 'deployment.yaml'
MANIFEST_FILENAME = 'manifest.yaml'
DOCKER_BUILD_DIR = 'docker'
IMPORT_NAME_CONFIGURE_PY = 'fastiot_configure'
BUILDER_NAME = 'fastiot_builder'
BUILD_MODE_DEBUG = 'debug'
BUILD_MODE_RELEASE = 'release'
BUILD_MODES = [BUILD_MODE_DEBUG, BUILD_MODE_RELEASE]

TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), 'templates')

FASTIOT_DOCKER_REGISTRY = 'FASTIOT_DOCKER_REGISTRY'
FASTIOT_DOCKER_REGISTRY_CACHE = 'FASTIOT_DOCKER_REGISTRY_CACHE'
FASTIOT_DEFAULT_TAG = 'FASTIOT_DEFAULT_TAG'
FASTIOT_NET = 'FASTIOT_NET'
FASTIOT_PULL_ALWAYS = 'FASTIOT_PULL_ALWAYS'
FASTIOT_PORT_OFFSET = 'FASTIOT_PORT_OFFSET'
FASTIOT_USE_PORT_IMPORT = 'FASTIOT_USE_PORT_IMPORT'
FASTIOT_CONFIGURE_FILE = 'FASTIOT_CONFIGURE_FILE'
