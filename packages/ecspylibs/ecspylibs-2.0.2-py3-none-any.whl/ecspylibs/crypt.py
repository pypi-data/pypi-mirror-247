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

from autologging import logged, traced
import logging

from dataclasses import dataclass
from typing import List, Optional
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import base64


@traced
@logged
@dataclass
class Crypt:
    """
    Doc String
    """

    key: Optional[str] = None
    key_size: Optional[int] = 32

    def __post_init__(self):
        """
        Doc String
        """

        assert self.key_size == 16 or self.key_size == 32

        if not self.key:
            self.key = get_random_bytes(self.key_size)

    def encrypt(self, plaintext: str):
        """
        Doc String
        """

        cipher = AES.new(self.key, AES.MODE_ECB)
        padtext = pad(plaintext.encode(), AES.block_size)
        ctext = cipher.encrypt(padtext)
        return base64.b64encode(ctext)

    def decrypt(self, ciphertext: str):
        """
        Doc String
        """

        cipher = AES.new(self.key, AES.MODE_ECB)
        decodedctext = base64.b64decode(ciphertext)
        padded_plaintext = cipher.decrypt(decodedctext)
        return unpad(padded_plaintext, AES.block_size).decode()

    @property
    def get_key(self):
        return self.key

    @property
    def get_key_size(self):
        return self.key_size
