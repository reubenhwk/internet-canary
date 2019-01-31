#!/usr/bin/env python

import sys
import logging

logging.basicConfig(stream=sys.stderr)

# WSGI insists on app being called application
from InternetCanaryWebApp import app as application
