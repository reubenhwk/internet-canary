#!/usr/bin/env python

import requests
import json
import sys
import time
import sqlite3
import speedtest

def _speedtest_probe():
    st = speedtest.Speedtest()
    st.get_best_server()
    down_speed = st.download(callback=speedtest.do_nothing)
    up_speed = st.upload(callback=speedtest.do_nothing)
    return down_speed, up_speed


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
                result real);
        ''')
        c.execute('''
            CREATE INDEX IF NOT EXISTS target_time ON results (target, time);
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS bandwidth_results (
                time real,
                down_speed integer,
                up_speed integer);
        ''')
        c.execute('''
            CREATE INDEX IF NOT EXISTS bandwidth_time ON bandwidth_results (time);
        ''')

        for url in config['canaries']['http']['targets']:
            now = time.time()
            result = _http_probe(url, 5)
            c.execute("INSERT INTO results (type, target, time, result) VALUES ('http', ?, ?, ?)", [url, now, result])

	bandwidth = _speedtest_probe()
        c.execute("INSERT INTO bandwidth_results (time, down_speed, up_speed) VALUES (?, ?, ?)", [now, bandwidth[0], bandwidth[1]])

        conn.commit()

        conn.close()

