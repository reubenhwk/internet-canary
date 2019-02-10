#!/usr/bin/env python3

import sys
import logging

logging.basicConfig(stream=sys.stderr)

# WSGI insists on app being called application
from InternetCanary.webapp import app as application
