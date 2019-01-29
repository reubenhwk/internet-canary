#!/usr/bin/env python

import requests
import json
import sys
import time

def http_probe(url, timeout):
    try:
        r = requests.get(url, timeout=timeout)
        if r.status_code == requests.codes.ok:
        	return r.elapsed.total_seconds()
    except:
        pass
    return -1

with open(sys.argv[1]) as configfile:
    config = json.load(configfile)

    with open(config['canaries']['http']['logfile'], 'a') as outfile:
        for target in config['canaries']['http']['targets']:
            url = "http://{}".format(target)
	    now = time.time()
            result = http_probe(url, 5)
            outfile.write("http, {}, {}, {}\n".format(now, url, result))
        
    with open(config['canaries']['https']['logfile'], 'a') as outfile:
        for target in config['canaries']['https']['targets']:
            url = "https://{}".format(target)
	    now = time.time()
            result = http_probe(url, 5)
            outfile.write("https, {}, {}, {}\n".format(now, url, result))
