#!/usr/bin/env python

import sys
import logging

logging.basicConfig(stream=sys.stderr)

# WSGI insists on app being called application
from helloflask import app as application
