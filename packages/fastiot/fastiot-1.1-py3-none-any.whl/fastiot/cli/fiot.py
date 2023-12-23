#!/usr/bin/env python3
""" Basic script to start the fiot command line program """
import logging
import os
import sys

from fastiot.cli import typer_app
from fastiot.cli.constants import CONFIGURE_FILE_NAME
from fastiot.env import env_basic
from fastiot.cli.model.project import ProjectContext  # noqa  # pylint: disable=wildcard-import,unused-wildcard-import


def main():
    # entry point for fastiot command
    logging.basicConfig(level=env_basic.log_level)

    # change work dir if configure.py is not in current dir
    curdir = os.path.abspath(os.path.curdir)
    entry_dir = curdir
    while os.path.isfile(os.path.join(curdir, CONFIGURE_FILE_NAME)) is False:
        newpath = os.path.abspath(os.path.join(curdir, '..'))
        if newpath == curdir:  # check if we reached system's root dir
            # reset current dir - we don't want to navigate to system's root dir unnecessarily
            curdir = entry_dir
            break
        curdir = newpath
    os.chdir(curdir)

    # import src dir if located and available
    _src_dir = os.path.join(curdir, 'src')
    if os.path.isdir(_src_dir) and _src_dir not in sys.path:
        sys.path.append(_src_dir)

    # trigger context creation
    context = ProjectContext.default  # pylint: disable=unused-variable

    typer_app.app()


if __name__ == '__main__':
    main()
