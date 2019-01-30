#!/usr/bin/env python

import InternetCanary
import time

while True:
    InternetCanary.run('/etc/internet-canary.d/internet-canary.json')
    time.sleep(300)
