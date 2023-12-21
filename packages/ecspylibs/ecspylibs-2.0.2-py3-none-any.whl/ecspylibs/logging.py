#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Do NOT edit this system file by hand -- use git.
# See "URL to git source" below.
#
# Author:        $Id: Thomas R. Stevenson <aa0026@wayne.edu> $
#
# Last Changed:  $Date: Tue Dec 19 15:33:04 2023 -0500 $
#
# URL to git source: $URL: git@git.wayne.edu:ECS_Projects/ECSpylibs.git $
#

"""
blah
"""

from dataclasses import dataclass
from typing import Optional
import logging
import logging.handlers
import autologging
import time
from autologging import logged, traced
from pathlib import Path, PosixPath


@traced
@logged
@dataclass
class Logging:
    """
    Blah
    """

    log_file: PosixPath
    log_level: Optional[str] = "warning"
    log_size: Optional[int] = 5 * (1024**2)
    log_count: Optional[int] = 5

    def __post_init__(self):
        """
        Blah
        """

        self.log_fmt = ""
        self.log_fmt += "%(asctime)s"
        self.log_fmt += " %(levelname)-7s"
        self.log_fmt += " [%(process)5d]"
        self.log_fmt += " %(module)s.py(%(funcName)s,%(lineno)d):"
        self.log_fmt += "\t%(message)s"

        self.log_levels = {
            "CRITICAL": logging.CRITICAL,
            "ERROR": logging.ERROR,
            "WARNING": logging.WARNING,
            "INFO": logging.INFO,
            "DEBUG": logging.DEBUG,
            "TRACE": autologging.TRACE,
        }

        self._log = logging.getLogger()
        self.set_level(self.log_level)

        self.fh = logging.handlers.RotatingFileHandler(
            self.log_file, maxBytes=int(self.log_size), backupCount=int(self.log_count)
        )

        self.formatter = logging.Formatter(self.log_fmt)
        self.fh.setFormatter(self.formatter)
        self._log.addHandler(self.fh)

    def set_level(self, log_level: str) -> bool:
        log_level = log_level.upper()
        if log_level in self.log_levels.keys():
            self.log_level = log_level
        else:
            raise ValueError(f"Invalid log level name: {log_level}.")

        self._log.setLevel(self.log_levels[self.log_level])
        return True
