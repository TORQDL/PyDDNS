#!/usr/bin/env python3

"""
    This is a python script for updating DNS records in Dreamhost or Cloudflare using their
    respective APIs.

    Provided under the MIT License (MIT). See LICENSE for details.
"""

"""
    Imports
"""
import logging
import time
import sys
import syslog
import os
import json
import urllib
import socket
import platform
from urllib.request import urlopen
# import requests
# import urllib.request as urlr
# import uuid
# import signal
# import threading
# import re
# import pandas as pd

"""
    Logging Level
"""
# Set logging level
logging.basicConfig(level=logging.DEBUG)

# Print the time for informational and debugging purposes
print("Current Time: ", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

"""
    Python Version Check
"""
if not (sys.version_info.major == 3 and sys.version_info.minor >= 5):
    print("PyDDNS requires Python 3.5 or higher!")
    print("You are using Python {}.{}.".format(sys.version_info.major, sys.version_info.minor))
    msg = 'PyDDNS requires Python 3.5 or higher! You are using Python {}.{}.'.format(sys.version_info.major, sys.version_info.minor)
    syslog.syslog(syslog.LOG_ERR, msg)
    sys.exit(msg)

"""
    Change to directory where script is
"""
# Changing directory to where the script is running from. Uncomment next print line for debug
# print("chdir to", sys.path[0])
os.chdir(sys.path[0])

"""
    DEMO_MODE
    You can set the demo mode to true, in which case, PyDDNS will only use sample_config.json
    and other sample configuration files based on the pattern sample_config*.json
    This mode is helpful when developing or troubleshooting PyDDNS.
"""
DEMO_MODE = True

"""
    IP Address Determinators
"""
def checkValidIP(ip, type):
    try:
        if type == "ipv4":
            socket.inet_pton(socket.AF_INET, ip)
        elif type == "ipv6":
            socket.inet_pton(socket.AF_INET6, ip)
        else:
            raise ValueError("IP type error, must be 'ipv4' or 'ipv6'")
        return True
    except socket.error:
        return False
def getIPs(use_local_ip, ipv4_enabled, ipv6_enabled):
    if use_local_ip:
        return getLocalIPs(ipv4_enabled, ipv6_enabled)
    else:
        return getPublicIPs(ipv4_enabled, ipv6_enabled)
def getLocalIPs(ipv4_enabled, ipv6_enabled):
    # get local IPs
    if platform.system() == "Linux":
        p = os.popen("hostname -I")
        ip_list = str(p.read()).strip().split(' ')
    elif platform.system() == "Windows":
        assert socket.gethostname()
        nets = socket.getaddrinfo(socket.gethostname(), None)
        assert nets
        ip_list = []
        for net in nets:
            ip_list.append(net[-1][0])
    else:
        raise ValueError("os type error, check result of platform.system()")
    ips = {}
    forbid_prefix = ["127.", "172.", "192.", "fe80:"]
    for ip in ip_list:
        if any(list(prefix in ip for prefix in forbid_prefix)):
            continue
        if ipv4_enabled and checkValidIP(ip, type="ipv4"):
            ips["ipv4"] = {
                "type": "A",
                "ip": ip
            }
        if ipv6_enabled and checkValidIP(ip, type="ipv6"):
            ips["ipv6"] = {
                "type": "AAAA",
                "ip": ip
            }
    return ips
def getPublicIPs(ipv4_enabled, ipv6_enabled):
    # get public IPs
    a = None
    aaaa = None
    if ipv4_enabled:
        try:
            a = requests.get("https://1.1.1.1/cdn-cgi/trace").text.split("\n")
            a.pop()
            a = dict(s.split("=") for s in a)["ip"]
        except Exception:
            deleteEntries("A")
    if ipv6_enabled:
        try:
            aaaa = requests.get(
                "https://[2606:4700:4700::1111]/cdn-cgi/trace").text.split("\n")
            aaaa.pop()
            aaaa = dict(s.split("=") for s in aaaa)["ip"]
        except Exception:
            deleteEntries("AAAA")
    ips = {}
    if(a is not None):
        ips["ipv4"] = {
            "type": "A",
            "ip": a
        }
    if(aaaa is not None):
        ips["ipv6"] = {
            "type": "AAAA",
            "ip": aaaa
        }
    return ips

"""
    Authentication
"""
def get_authentication(DNS_Provider):
    AUTH = []
    PROVIDER = DNS_Provider['provider']

    if PROVIDER == 'cloudflare':
        if 'api_key' in DNS_Provider['authentication'] and DNS_Provider['authentication']['api_key']:
            AUTH.append(DNS_Provider['authentication']['api_key'])
        else:
            msg = 'The Cloudflare API key is missing or blank. Please edit your PyDDNS configuration and try again.'
            syslog.syslog(syslog.LOG_ERR, msg)
            sys.exit(msg)
        if 'account_email' in DNS_Provider['authentication'] and DNS_Provider['authentication']['account_email']:
            AUTH.append(DNS_Provider['authentication']['account_email'])
        else:
            msg = 'The Cloudflare account email is missing or blank. Please edit your PyDDNS configuration and try again.'
            syslog.syslog(syslog.LOG_ERR, msg)
            sys.exit(msg)
        if 'api_token' in DNS_Provider['authentication'] and DNS_Provider['authentication']['api_token']:
            AUTH.append(DNS_Provider['authentication']['api_token'])
        else:
            msg = 'The Cloudflare API token is missing or blank. Please edit your PyDDNS configuration and try again.'
            syslog.syslog(syslog.LOG_ERR, msg)
            sys.exit(msg)

    elif PROVIDER == 'dreamhost':
        if 'api_key' in DNS_Provider['authentication'] and DNS_Provider['authentication']['api_key']:
            AUTH.append(DNS_Provider['authentication']['api_key'])
        else:
            msg = 'The Dreamhost API key is missing or blank. Please edit your PyDDNS configuration and try again.'
            syslog.syslog(syslog.LOG_ERR, msg)
            sys.exit(msg)

    else:
        msg = 'The DNS provider cannot be recognized. Only Dreamhost and Cloudflare are currently supported. Please edit your PyDDNS configuration and try again.'
        syslog.syslog(syslog.LOG_ERR, msg)
        sys.exit(msg)
    return AUTH

"""
    Cloudflare Updater
"""
def update_dns_cloudflare(AUTH, ZONEID, RECORD):
    print("\nCloudflare Info:\nAuth: ", AUTH, "\nZone: ", ZONEID, "\nRecord: ", RECORD)

"""
    Dreamhost Updater
"""
def update_dns_dreamhost(AUTH, RECORD):
    print("\nDreamhost Info:\nAuth: ", AUTH, "\nRecord: ", RECORD)

"""
    Process DNS Provider Info
"""
def process_providers_from_json(CONFIG_DATA):
    # read each DNS provider entry
    for PROVIDER_INDEX, DNS_PROVIDER in enumerate(CONFIG_DATA['dns']):
        PROVIDER = DNS_PROVIDER['provider']
        
        AUTH = get_authentication(DNS_PROVIDER)
        # return should contain [API_Key, Account_Email, API_Token]

        # check which provider and process the records accordingly
        if PROVIDER == 'cloudflare':
            for ZONE_INDEX, ZONE in enumerate(DNS_PROVIDER['zones']):
                ZONEID = ZONE['zone_id']

                for RECORD_INDEX, RECORD in enumerate(ZONE['records']):
                    update_dns_cloudflare(AUTH, ZONEID, RECORD)

        elif PROVIDER == 'dreamhost':
            for RECORD_INDEX, RECORD in enumerate(DNS_PROVIDER['records']):
                update_dns_dreamhost(AUTH, RECORD)

"""
    Process local .json configuration files
"""
def process_local_json(PATH_TO_CONFIG_FILES, CONFIG_FILES):
    # we need both the json and an index number so use enumerate()
    for JSON_FILE_INDEX, CONFIG_FILE in enumerate(CONFIG_FILES):
        with open(os.path.join(PATH_TO_CONFIG_FILES, CONFIG_FILE)) as JSON_FILE:
            CONFIG_DATA = json.load(JSON_FILE)
            process_providers_from_json(CONFIG_DATA)

def process_online_json():
    if DEMO_MODE:
        print("\nPyDDNS cannot find sample config files. It will use the sample from the PyDDNS GitHub repository.")
        url = "https://raw.githubusercontent.com/TORQDL/pyddns/initial_build/config/sample_config.json"
        CONFIG_DATA = json.loads(urlopen(url).read().decode("UTF-8"))
        process_providers_from_json(CONFIG_DATA)

"""
    Start Script
"""
def make_it_so():
    PATH_TO_CONFIG_FILES = os.getcwd() + "/config/"
    if DEMO_MODE:
        print("\nPyDDNS is running in Demo mode. Only sample config files will be used, such as sample_config.json and sample_config2.json")
        # if os.path.exists(PATH_TO_CONFIG_FILES):
        #     CONFIG_FILES = [FILE_NAME for FILE_NAME in os.listdir(PATH_TO_CONFIG_FILES) if FILE_NAME.startswith('sample_config') and FILE_NAME.endswith('.json')]
        #     if CONFIG_FILES:
        #         process_local_json(PATH_TO_CONFIG_FILES, CONFIG_FILES)
        #     else:
        #         process_online_json()
        # else:
        #     process_online_json()
        process_online_json()
    else:
        if os.path.exists(PATH_TO_CONFIG_FILES):
            CONFIG_FILES = [FILE_NAME for FILE_NAME in os.listdir(PATH_TO_CONFIG_FILES) if FILE_NAME.endswith('.json')]
            process_local_json(PATH_TO_CONFIG_FILES, CONFIG_FILES)
        else:
            msg = 'PyDDNS cannot find or cannot access the ', PATH_TO_CONFIG_FILES, ' directory to access the configuration files.'
            syslog.syslog(syslog.LOG_ERR, msg)
            sys.exit(msg)

#### Let's do it!
make_it_so()