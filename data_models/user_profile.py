# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.


class UserProfile:
    def __init__(self, mac: str = None, lookup: int = 0, action: str = None):
        self.mac = mac
        self.lookup = lookup 
        self.action = action
