#!/usr/bin/env python3
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

from dataclasses import dataclass
from pathlib import Path, PosixPath
import pickle
import sys
from autologging import logged, traced
from ecspylibs.configfile import *
from ecspylibs.crypt import Crypt


@traced
@logged
@dataclass
class Password:
    """Add, Delete, or return User ID and Password information stored in an application PW file."""

    passwd_file: PosixPath = None

    def __post_init__(self):
        """Set up the Password environment."""

        if self.passwd_file.exists():
            try:
                self.cf = config_file(self.passwd_file)
                self.data = self.cf.read
                self.secret = self.data["secret"]
                self.passwd = self.data["passwd"]
                self.passwd_crypt = Crypt(key=self.secret)
                self.__log.debug(
                    "Successfully read the password file '%s'.", self.passwd_file
                )
            except Exception as e:
                self.__log.exception("Exception: '%s'", e)
                raise e

        elif self.passwd_file.parent.exists():
            self.passwd_file.touch()
            self.passwd_crypt = Crypt()
            self.secret = self.passwd_crypt.get_key
            self.passwd = {}
            self.update()

        else:
            raise ValueError("Invalid file name and/or directory location.")

    def update(self) -> bool:
        """Update the PW file."""

        try:
            self.data = {"secret": self.secret, "passwd": self.passwd}
            pickle.dump(self.data, open(self.passwd_file, "wb"))
        except Exception as e:
            self.__log.exception("Exception: '%s'", e)
            raise e

        return True

    def set(self, user_id: object, passwd: object) -> bool:
        """Add/Modify a User/PW entry in the PW file."""

        try:
            self.passwd[user_id] = self.passwd_crypt.encrypt(passwd)
            self.update()
        except Exception as e:
            self.__log.exception("Exception: '%s'", e)
            raise e

        return True

    def get(self, user_id: object) -> str:
        """Verify and return, if exists, the PW for the given ID."""

        if user_id in self.passwd:
            user_pw = self.passwd_crypt.decrypt(self.passwd[user_id])
        else:
            user_pw = ""

        return user_pw

    def delete(self, user_id: object) -> bool:
        """Verify and delete a ID/PW entry in the PW file."""

        if user_id in self.passwd:
            self.__log.warning("Deleting User id '%s'.", user_id)
            del self.passwd[user_id]
            self.update()
        else:
            self.__log.warning("Id '%s' does not exists.", user_id)

        return True

    @property
    def list_ids(self) -> bool:
        """Generate a list of User ID in the PW file."""

        print(f"ID", file=sys.stdout)
        user_ids = list(self.passwd)
        user_ids.sort()
        for user_id in user_ids:
            print(f"{user_id:<10}", file=sys.stdout)

        return True

    @property
    def list_pws(self) -> bool:
        """Generate a list of User ID and Passwords in the PW file."""

        print(f"{'ID':<15} Password", file=sys.stdout)
        user_ids = list(self.passwd)
        user_ids.sort()
        for user_id in user_ids:
            user_pw = self.get(user_id)
            print(f"{user_id:<15} {user_pw}", file=sys.stdout)

        return True
