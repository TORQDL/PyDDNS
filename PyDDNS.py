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

def make_it_so():

#### Let's do it!
make_it_so()