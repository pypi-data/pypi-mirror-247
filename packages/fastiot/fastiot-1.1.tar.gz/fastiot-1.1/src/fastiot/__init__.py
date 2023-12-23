"""
FastIoT Library
===============
"""
from fastiot.cli.version import get_version
from fastiot.core.logger import logging
from fastiot.cli.commands import *
from fastiot.cli.common.docker_templates import *
from fastiot.cli.common import infrastructure_services

try:
    from fastiot.__version__ import __version__
except ImportError:
    __version__ = get_version(complete=True)
