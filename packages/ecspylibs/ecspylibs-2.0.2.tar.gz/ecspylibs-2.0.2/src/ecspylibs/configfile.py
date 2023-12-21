#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Do NOT edit this system file by hand -- use git.  See "URL to git source" below.
#
# Author:        $Id: Thomas R. Stevenson <aa0026@wayne.edu> $
#
# Last Changed:  $Date: Tue Dec 19 15:33:04 2023 -0500 $
#
# URL to git source: $URL: git@git.wayne.edu:ECS_Projects/ECSpylibs.git $
#

"""
Doc String
"""

import sys

from autologging import logged, traced
import logging

from abc import ABC, abstractmethod
from configparser import ConfigParser
from json.decoder import JSONDecodeError
from pathlib import Path, PosixPath
from typing import List, Optional
import pickle

import json
import toml
import xmltodict
import yaml

from lxml.etree import XMLSyntaxError
from toml.decoder import TomlDecodeError
from yaml.parser import ParserError
from yaml.scanner import ScannerError


@traced
@logged
class ConfigFileABC(ABC):
    """
    Doc String
    """

    @abstractmethod
    def read(self) -> object:
        pass

    @abstractmethod
    def name(self) -> object:
        pass


@traced
@logged
class ConfigFileIni(ConfigFileABC):
    """
    Doc String
    """

    def __init__(self, file: PosixPath):
        self.file = file
        self.__log.debug(f"File : {self.file}")

    @property
    def read(self) -> object:
        config = ConfigParser()
        try:
            config.read(self.file)
        except Exception as e:
            print(
                f"\nException error processing file '{self.file}'.\n", file=sys.stderr
            )
            raise e
        data = {}
        for section in config.sections():
            data[section] = {}
            for key, value in config.items(section):
                data[section][key] = value
        return data

    @property
    def name(self) -> object:
        return self.file


@traced
@logged
class ConfigFileJson(ConfigFileABC):
    """
    Doc String
    """

    def __init__(self, file: PosixPath):
        self.file = file
        self.__log.debug(f"File : {self.file}")

    @property
    def read(self) -> object:
        try:
            with open(self.file, "r") as f:
                return json.load(f)
        except JSONDecodeError as e:
            print(
                f"\nJSON decode error while parsing file '{self.file}'.\n",
                file=sys.stderr,
            )
            raise e
        except UnicodeDecodeError as e:
            print(
                f"\nUnicode decode error while parsing file '{self.file}'.\n",
                file=sys.stderr,
            )
            raise e
        except Exception as e:
            print(
                f"\nException error processing file '{self.file}'.\n", file=sys.stderr
            )
            raise e

    @property
    def name(self) -> object:
        return self.file


@traced
@logged
class ConfigFilePW(ConfigFileABC):
    """
    Doc String
    """

    def __init__(self, file: PosixPath):
        self.file = file
        self.__log.debug(f"File : {self.file}")

    @property
    def read(self) -> object:
        try:
            return pickle.load(open(self.file, "rb"))
        except Exception as e:
            print(
                f"\nException error processing password file '{self.file}'.\n",
                file=sys.stderr,
            )
            raise e

    @property
    def name(self) -> object:
        return self.file


@traced
@logged
class ConfigFileToml(ConfigFileABC):
    """
    Doc String
    """

    def __init__(self, file: PosixPath):
        self.file = file
        self.__log.debug(f"File : {self.file}")

    @property
    def read(self) -> object:
        try:
            return toml.load(self.file)
        except TomlDecodeError as e:
            print(
                f"\nTOML decode error while parsing file '{self.file}'.\n",
                file=sys.stderr,
            )
            raise e
        except UnicodeDecodeError as e:
            print(
                f"\nUnicode decode error while parsing file '{self.file}'.\n",
                file=sys.stderr,
            )
            raise e
        except Exception as e:
            print(
                f"\nException error processing file '{self.file}'.\n", file=sys.stderr
            )
            raise e

    @property
    def name(self) -> object:
        return self.file


@traced
@logged
class ConfigFileYaml(ConfigFileABC):
    """
    Doc String
    """

    def __init__(self, file: PosixPath):
        self.file = file
        self.__log.debug(f"File : {self.file}")

    @property
    def read(self) -> object:
        try:
            with open(self.file, "r") as f:
                return yaml.safe_load(f)
        except ParserError as e:
            print(
                f"\nYAML parse error while parsing file '{self.file}'.\n",
                file=sys.stderr,
            )
            raise e
        except ScannerError as e:
            print(
                f"\nYAML Scanner error while parsing file '{self.file}'.\n",
                file=sys.stderr,
            )
            raise e
        except UnicodeDecodeError as e:
            print(
                f"\nUnicode decode error while parsing file '{self.file}'.\n",
                file=sys.stderr,
            )
            raise e
        except Exception as e:
            print(
                f"\nException error processing file '{self.file}'.\n", file=sys.stderr
            )
            raise e

    @property
    def name(self) -> object:
        return self.file


@traced
@logged
class ConfigFileXml(ConfigFileABC):
    """
    Doc String
    """

    def __init__(self, file: PosixPath):
        self.file = file
        self.__log.debug(f"File : {self.file}")

    @property
    def read(self) -> object:
        try:
            with open(self.file) as f:
                return xmltodict.parse(f.read())
        except XMLSyntaxError as e:
            print(
                f"\nXML Syntax error while parsing file '{self.file}'.\n{e}\n",
                file=sys.stderr,
            )
            raise e
        except Exception as e:
            print(
                f"\nException error processing file '{self.file}'.\n{e}\n",
                file=sys.stderr,
            )
            raise e

    @property
    def name(self) -> object:
        return self.file


config_file_types = {
    ".ini": ConfigFileIni,
    ".json": ConfigFileJson,
    ".pw": ConfigFilePW,
    ".toml": ConfigFileToml,
    ".xml": ConfigFileXml,
    ".yaml": ConfigFileYaml,
    ".yml": ConfigFileYaml,
}


@traced
@logged
def config_file(
    file: PosixPath, directories: Optional[List[PosixPath]] = None
) -> ConfigFileABC:
    """
    Doc string
    """

    suffix = file.suffix
    directory = None

    if file.parent.exists():
        if file.is_absolute():
            directory = file.parent
        elif file.parent == PosixPath(".") and directories:
            for dir in directories:
                if dir.is_dir:
                    if not directory:
                        directory = dir

                    if (dir / file).exists():
                        file = dir / file
                        directory = dir
                        break
            else:
                if directory:
                    return directory
                else:
                    raise ValueError("Invalid directory name list locations.")
        elif file.exists():
            directory = file.cwd() / file.parent
            file = directory / file.name
        else:
            return file
    else:
        raise ValueError("Invalid directory name location.")

    if suffix in config_file_types.keys():
        return config_file_types[suffix](file)
    else:
        raise ValueError("Invalid configure type.")
