#!/usr/bin/env python3
#
#  __init__.py

"""
a more powerful whiptail python wrapper.
"""
#  Licensed under the Apache License. See LICENSE file for details.
#
#  Docstrings based on the whiptail manpage
#  https://manpages.debian.org/buster/whiptail/whiptail.1.en.html
#  Written by
#      XUranus <2257238649wdx@gmail.com>
#

# stdlib
from __future__ import annotations
from typing import Optional, Sequence, Type
import subprocess
import shutil

# third party
from .whiptail_box import *

__author__: str = "XUranus"
__copyright__: str = ""
__license__: str = "Apache"
__version__: str = "0.1.0"
__email__: str = "2257238649wdx@gmail.com"

__all__ = ["Response", "Whiptail"]

"""
    TODO_LIST:
        --output-fd <fd>           output to fd, not stdout
"""