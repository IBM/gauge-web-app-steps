#
# Copyright IBM Corp. 2019-
# SPDX-License-Identifier: MIT
#

import time
import subprocess
import requests

from getgauge.python import data_store

from .config import saucelabs_config
from .config import common_config as config
from .driver.platform import Platform
from .driver.operating_system import OperatingSystem


class SauceTunnel:
    """
    This class encapsulates the interaction with the Sauce Connect Proxy.
    """

    @staticmethod
    def _wait_for_sc_readiness():
        sauce_status_address = saucelabs_config.get_sauce_status_address()
        readiness_url = f"http://{sauce_status_address}/readiness"
        response_readiness = requests.get(readiness_url)
        while not response_readiness.ok:
            time.sleep(2)
            response_readiness = requests.get(readiness_url)
        time.sleep(3) # usually the readiness check is too fast

    @staticmethod
    def start():
        sauce_active = saucelabs_config.is_sauce_tunnel_active()
        platform = config.get_platform()
        if not sauce_active or platform != Platform.SAUCELABS:
            return
        sauce_path = saucelabs_config.get_sauce_path()
        sauce_user = saucelabs_config.get_sauce_user_name()
        sauce_key = saucelabs_config.get_sauce_access_key()
        sauce_region = saucelabs_config.get_sauce_region()
        sauce_tunnel = saucelabs_config.get_tunnel_name()
        sauce_status = saucelabs_config.get_sauce_status_address()
        sauce_dns = saucelabs_config.get_sauce_dns() # dns server from VPN connection
        sauce_no_ssl_bump_domains = saucelabs_config.get_sauce_no_ssl_bump_domains()
        sauce_log_file = saucelabs_config.get_sauce_log_file()
        sc_call = (f"{sauce_path} -u {sauce_user} -k {sauce_key} --region {sauce_region} "
            f"--tunnel-name {sauce_tunnel} --status-address {sauce_status} --logfile {sauce_log_file}")
        if sauce_dns:
            sc_call += f" --dns {sauce_dns}"
        if sauce_no_ssl_bump_domains:
            sc_call += f" --no-ssl-bump-domains {sauce_no_ssl_bump_domains}"
        if saucelabs_config.is_sauce_tunnel_pooling():
            sc_call += " --tunnel-pool"
        if saucelabs_config.get_host_os() is not OperatingSystem.WINDOWS:
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
