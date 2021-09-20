#!/usr/bin/env python3

""" 
    This is a python script for updating DNS records in Dreamhost or Cloudflare using their
    respective APIs.

    Provided under the MIT License (MIT). See LICENSE for details.
"""

#Python version check
import sys
import syslog
if sys.version_info.major < 3:
    msg = 'This script requires Python 3. It cannot run. Please install Python 3 and try again.'
    syslog.syslog(syslog.LOG_ERR, msg)
    sys.exit(msg)

import urllib.request as urlr
import uuid
import logging
import json
# import requests
import json
import sys
import signal
import os
import time
import threading
import re
import socket
import platform
# import pandas as pd

# Set logging level
logging.basicConfig(level=logging.DEBUG)

# Set demo mode
DEMO_MODE = True

def get_authentication(DNS_Provider):
    AUTH = []
    PROVIDER = DNS_Provider['provider']
    if PROVIDER == 'cloudflare':
        logging.debug("Getting Authentication for Cloudflare...")
        if 'api_key' in DNS_Provider['authentication'] and DNS_Provider['authentication']['api_key']:
            AUTH.append(DNS_Provider['authentication']['api_key'])
        else:
            logging.error("Cloudflare API key is missing or blank...")
            msg = 'The Cloudflare API key is missing or blank. Please edit your PyDDNS configuration and try again.'
            syslog.syslog(syslog.LOG_ERR, msg)
            sys.exit(msg)
        if 'account_email' in DNS_Provider['authentication'] and DNS_Provider['authentication']['account_email']:
            AUTH.append(DNS_Provider['authentication']['account_email'])
        else:
            logging.error("Cloudflare account email is missing or blank...")
            msg = 'The Cloudflare account email is missing or blank. Please edit your PyDDNS configuration and try again.'
            syslog.syslog(syslog.LOG_ERR, msg)
            sys.exit(msg)
        if 'api_token' in DNS_Provider['authentication'] and DNS_Provider['authentication']['api_token']:
            AUTH.append(DNS_Provider['authentication']['api_token'])
        else:
            logging.error("Cloudflare API token is missing or blank...")
            msg = 'The Cloudflare API token is missing or blank. Please edit your PyDDNS configuration and try again.'
            syslog.syslog(syslog.LOG_ERR, msg)
            sys.exit(msg)
    elif PROVIDER == 'dreamhost':
        logging.debug("Getting Authentication for Dreamhost...")
        if 'api_key' in DNS_Provider['authentication']:
            AUTH.append(DNS_Provider['authentication']['api_key'])
        else:
            logging.error("Dreamhost API key is missing or blank...")
            msg = 'The Dreamhost API key is missing or blank. Please edit your PyDDNS configuration and try again.'
            syslog.syslog(syslog.LOG_ERR, msg)
            sys.exit(msg)
    else:
        logging.error("Cannot get authentication parameters. DNS provider not recognized...")
        msg = 'The DNS provider cannot be recognized. Please edit your PyDDNS configuration and try again.'
        syslog.syslog(syslog.LOG_ERR, msg)
        sys.exit(msg)
    
    return AUTH

def update_dns_cloudflare():
    logging.debug("Updating Cloudflare DNS...")

def update_dns_dreamhost():
    logging.debug("Updating Dreamhost DNS...")

def make_it_so():

    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    # print("chdir to", sys.path[0])
    os.chdir(sys.path[0])
    # check python version
    version = float(str(sys.version_info[0]) + "." + str(sys.version_info[1]))
    if(version < 3.5):
        raise Exception("This script requires Python 3.5+")
        
    # this finds our json config files
    PATH_TO_CONFIG_FILES = os.getcwd() + "/config/"
    if DEMO_MODE:
        logging.info("Running in Demo mode, so only finding sample config file, such as sample_config.json and sample_config2.json")
        CONFIG_FILES = [FILE_NAME for FILE_NAME in os.listdir(PATH_TO_CONFIG_FILES) if FILE_NAME.startswith('sample_config') and FILE_NAME.endswith('.json')]
    else:
        CONFIG_FILES = [FILE_NAME for FILE_NAME in os.listdir(PATH_TO_CONFIG_FILES) if FILE_NAME.endswith('.json')]

    # we need both the json and an index number so use enumerate()
    for JSON_FILE_INDEX, CONFIG_FILE in enumerate(CONFIG_FILES):
        with open(os.path.join(PATH_TO_CONFIG_FILES, CONFIG_FILE)) as JSON_FILE:
            CONFIG_DATA = json.load(JSON_FILE)
            logging.debug("\n\nConfig data:\n%s", CONFIG_DATA)

            # read each DNS provider entry
            for Provider_Index, DNS_Provider in enumerate(CONFIG_DATA['dns']):
                logging.debug("\n\n%s:%s", Provider_Index, DNS_Provider['provider'])
                PROVIDER = DNS_Provider['provider']
                
                AUTH = get_authentication(DNS_Provider)
                logging.debug("Authentication: %s", AUTH)
                # return should contain [API_Key, Account_Email, API_Token]

                # check which provider and process accordingly
                if PROVIDER == 'cloudflare':
                    # TODO itterate over zone info
                    # TODO itterate over records in each zone
                    update_dns_cloudflare(AUTH, ZONE, RECORD)
                elif PROVIDER == 'dreamhost':
                    # TODO itterate over records
                    update_dns_dreamhost(AUTH, RECORD)

#### Let's do it!
make_it_so()