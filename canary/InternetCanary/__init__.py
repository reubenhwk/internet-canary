#!/usr/bin/env python

import requests
import json
import sys
import time
import sqlite3

def _http_probe(url, timeout):
    try:
        r = requests.get(url, timeout=timeout)
        if r.status_code == requests.codes.ok:
            return r.elapsed.total_seconds()
    except:
        pass
    return -1

def run(config_file_path):
    with open(config_file_path) as configfile:
        config = json.load(configfile)

        conn = sqlite3.connect(config['output'])
        c = conn.cursor()

        c.execute('''
            CREATE TABLE IF NOT EXISTS results (
                id integer primary key,
                type text,
                target text,
                time real,
                result real)
        ''')

        for url in config['canaries']['http']['targets']:
            now = time.time()
            result = _http_probe(url, 5)
            c.execute("INSERT INTO results (type, target, time, result) VALUES ('http', ?, ?, ?)", [url, now, result])
        conn.commit()

        conn.close()

