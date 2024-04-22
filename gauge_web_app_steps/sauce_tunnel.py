#
# Copyright IBM Corp. 2019-
# SPDX-License-Identifier: MIT
#

import os
import requests
import subprocess
import time

from getgauge.python import data_store

from .config import saucelabs_config
from .config import common_config as config
from .driver.platform import Platform


class SauceTunnel:
    """
    This class encapsulates the interaction with the Sauce Connect Proxy.
    The tunnel can be configured with environment variables.
    Overview of configuration options: https://docs.saucelabs.com/secure-connections/sauce-connect-5/operation/configuration/
    """

    @staticmethod
    def _wait_for_sc_readiness():
        sauce_api_address = saucelabs_config.get_sauce_api_address()
        readiness_url = f"http://{sauce_api_address}/readyz"
        for _ in range(30):
            try:
                with requests.get(readiness_url) as response_readiness:
                    if response_readiness.status_code == 200 and response_readiness.text == 'OK':
                        print("Sauce Connect up")
                        time.sleep(10) # usually the readiness check is too fast
                        return
                time.sleep(2)
            except requests.RequestException:
                time.sleep(2)
        raise Exception("Sauce Connect tunnel could not be established")

    @staticmethod
    def start():
        sauce_active = saucelabs_config.is_sauce_tunnel_active()
        platform = config.get_platform()
        if not sauce_active or platform != Platform.SAUCELABS:
            return
        sauce_path = saucelabs_config.get_sauce_path()
        sc_call = f"{sauce_path} run"
        if os.name == "posix":
            sc_call = sc_call.split(" ")
        print("Starting Sauce Connect Tunnel")
        sauce_connect = subprocess.Popen(sc_call)
        data_store.suite['_sauce_connect'] = sauce_connect
        time.sleep(5)
        SauceTunnel._wait_for_sc_readiness()

    @staticmethod
    def terminate():
        sauce_connect: subprocess.Popen = data_store.suite.get('_sauce_connect')
        if sauce_connect:
            print("Terminating Sauce Connect tunnel")
            sauce_connect.terminate()
            for _ in range(10):
                time.sleep(1)
                if sauce_connect.poll() is not None:
                    return
            print("Killing Sauce Connect tunnel")
            sauce_connect.kill()
