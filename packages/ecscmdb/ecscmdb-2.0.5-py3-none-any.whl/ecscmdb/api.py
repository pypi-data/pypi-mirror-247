#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Do NOT edit this system file by hand -- use git.
# See "URL to git source" below.
#
# Author:        $Id: Thomas R. Stevenson <aa0026@wayne.edu> $
#
# Last Changed:  $Date: Wed Dec 20 17:46:02 2023 -0500 $
#
# URL to git source: $URL: git@git.wayne.edu:ECS_Projects/ECScmdb.git $
#

from dataclasses import dataclass
from typing import List, Optional
from autologging import logged, traced
from io import StringIO

import json
import sys
import time
import pandas as pd
import requests

from ecspylibs.password import Password
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


@traced
@logged
@dataclass
class API:
    """Verify blah blah blah."""

    ome_user: str
    ome_pw: str
    ome_host: str

    def __post_init__(self) -> None:
        """Set up the CheckService environment."""

        self.inventory_types_url = None
        self.inventory_details_url = None
        self.device_id = None
        self.device_response = None
        self.session_info = None

        self.headers = {
            "content-type": "application/json",
        }

        self.user_creds = {
            "UserName": self.ome_user,
            "Password": self.ome_pw,
            "SessionType": "API",
        }

        self.__log.debug(f"User            : '{self.ome_user}'")
        self.__log.debug(f"Pass            : '{self.ome_pw}'")
        self.__log.debug(f"Host            : '{self.ome_host}'")
        self.__log.debug(
            f"OMESessionURL   : 'https://{self.ome_host}/api/SessionService/Sessions'"
        )
        self.__log.debug(
            f"OMEDeviceURL    : 'https://{self.ome_host}/api/DeviceService/Devices'"
        )

    def login(self) -> bool:
        """Blah."""
        try:
            self.session_info = requests.post(
                f"https://{self.ome_host}/api/SessionService/Sessions",
                verify=False,
                data=json.dumps(self.user_creds),
                headers=self.headers,
            )
            self.__log.debug(
                f"sessionInfo.status_code = '{self.session_info.status_code}'"
            )
            self.__log.debug(f"sessionInfo.headers")
            for self.i in self.headers.keys():
                self.__log.debug(
                    f"\tsessionInfo.headers[{self.i}] = '{self.headers[self.i]}'"
                )
        except Exception as e:
            print(f"Exception: '{e}'.", file=sys.stderr)
            self.__log.critical(f"Fatal error occurred while something.")
            self.__log.exception(f"Exception: '{e}'.")
            return False

        self.__log.debug(f"sessionInfo.status_code = '{self.session_info.status_code}'")
        if self.session_info.status_code == 201:
            self.headers["X-Auth-Token"] = self.session_info.headers["X-Auth-Token"]
        else:
            print(
                f"Unable to create a session with appliance {self.ome_host}",
                file=sys.stderr,
            )
            self.__log.error(
                f"Unable to create a session with appliance {self.ome_host}"
            )
            return False

        return True

    def _get_device_list(self, next_link: object = None) -> bool:
        """Verify blah blah blah"""

        if next_link:
            self.__log.debug(f"nextLink : '{next_link}'")
            self.URL = f"https://{self.ome_host}{next_link}"
        else:
            self.__log.debug(f"nextLink : None")
            self.URL = f"https://{self.ome_host}/api/DeviceService/Devices"

        self.__log.debug(f"self.URL : '{self.URL}'")

        try:
            self.device_response = requests.get(
                self.URL, verify=False, headers=self.headers
            )
            self.__log.debug(
                f"deviceResponse.status_code = '{self.device_response.status_code}'"
            )
        except Exception as e:
            print(f"Exception: '{e}.", file=sys.stderr)
            self.__log.critical(f"Fatal error occurred while something.")
            self.__log.exception(f"Exception: '{e}'.")
            return False

        if self.device_response.status_code == 200:
            return json.dumps(self.device_response.json(), indent=4, sort_keys=True)
        else:
            print(
                f"Unable to retrieve device list from {self.ome_host}", file=sys.stderr
            )
            self.__log.error(f"Unable to retrieve device list from {self.ome_host}")
            return False

    def get_device_list(self) -> object:
        """Verify blah blah blah"""

        ome_list = self._get_device_list()

        dl = pd.read_json(StringIO(ome_list))

        dl_temp = dl

        while "@odata.nextLink" in dl_temp.keys():
            next_link = dl_temp["@odata.nextLink"][0]
            ome_list = self._get_device_list(next_link=next_link)
            dl_temp = pd.read_json(StringIO(ome_list))
            dl = pd.concat([dl, dl_temp])

        return dl

    def get_inventory_details(self, device_id: object) -> list:
        """Verify blah blah blah"""

        self.device_id = device_id
        self.__log.debug(f"deviceId : '{self.device_id}'")

        self.inventory_details_url = f"https://{self.ome_host}/api/DeviceService/Devices({self.device_id})/InventoryDetails"
        self.__log.debug(f"url : '{self.inventory_details_url}'")

        self.__log.debug(f"Calling requests.get: {self.inventory_details_url=}")
        start_time = time.perf_counter()

        try:
            self.device_response = requests.get(
                self.inventory_details_url, verify=False, headers=self.headers
            )
        except Exception as e:
            print(f"Exception: '{e}'.", file=sys.stderr)
            self.__log.critical(f"Fatal error occurred while something.")
            self.__log.exception(f"Exception: '{e}'.")
            return [self.device_id, False]

        finish_time = time.perf_counter()
        run_time = finish_time - start_time
        self.__log.info(
            f"It took {run_time} seconds, Start({start_time}) to End({finish_time}), to retrive info for device {self.device_id}."
        )

        self.__log.debug(
            f"self.deviceResponse.status_code({self.device_id}) = {self.device_response.status_code}"
        )

        if self.device_response.status_code == 200:
            return [
                self.device_id,
                json.dumps(self.device_response.json(), indent=4, sort_keys=True),
            ]
        else:
            print(
                f"Unable to retrieve device list from {self.ome_host}", file=sys.stderr
            )
            self.__log.debug(
                f"self.deviceResponse.status_code({self.device_id}) = {self.device_response.status_code}"
            )
            self.__log.error(
                f"Unable to retrieve device list from {self.ome_host}", self.ome_host
            )
            return [self.device_id, False]

    def get_inventory_types(self, device_id: object) -> object:
        """Verify blah blah blah"""

        self.device_id = device_id
        self.__log.debug(f"deviceId : '{self.device_id}'")

        self.inventory_types_url = f"https://{self.ome_host}/api/DeviceService/Devices({self.device_id})/InventoryTypes"
        self.__log.debug(f"url : '{self.inventory_types_url}'")

        try:
            self.device_response = requests.get(
                self.inventory_types_url, verify=False, headers=self.headers
            )
            self.__log.debug(
                f"deviceResponse.status_code = '{self.device_response.status_code}'"
            )
        except Exception as e:
            print(f"Exception: '{e}'.", file=sys.stderr)
            self.__log.critical(f"Fatal error occurred while something.")
            self.__log.exception(f"Exception: '{e}'.")
            return False

        if self.device_response.status_code == 200:
            return json.dumps(self.device_response.json(), indent=4, sort_keys=True)
        else:
            print(
                f"Unable to retrieve device list from {self.ome_host}", file=sys.stderr
            )
            self.__log.error(f"Unable to retrieve device list from {self.ome_host}")
            return False
