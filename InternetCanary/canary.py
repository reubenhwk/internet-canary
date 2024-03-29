#!/usr/bin/env python3

import pathlib
import requests
import speedtest
import sqlite3
import sys
import time
import dns.resolver
import logging as log

def probe_dns(hostname, record_type):
    resolver = dns.resolver.Resolver()
    start = time.time()
    resolver.query(hostname, record_type)
    end = time.time()
    return end - start

def probe_speedtest():
    st = speedtest.Speedtest()
    st.get_best_server()
    down_speed = st.download(callback=speedtest.do_nothing)
    up_speed = st.upload(callback=speedtest.do_nothing)
    return down_speed, up_speed


def probe_http(url, timeout):
    r = requests.get(url, timeout=timeout)
    if r.status_code == requests.codes.ok:
        return r.elapsed.total_seconds()

def canary_dns(db, targets):
    cursor = db.cursor()
    for target in targets:
        now = time.time()
        try:
            result = probe_dns(target, 'A')
            cursor.execute('''
               INSERT INTO dns_canary_results (target, time, result)
               VALUES (?, ?, ?)
            ''', [target, now, result])
        except:
            log.warn('dns canary failed on {}...'.format(target))
            pass

def canary_http(db, targets):
    cursor = db.cursor()
    for target in targets:
        now = time.time()
        try:
            result = probe_http(target, 5)
            cursor.execute('''
               INSERT INTO http_canary_results (target, time, result)
               VALUES (?, ?, ?)
            ''', [target, now, result])
        except:
            log.warn('http canary failed on {}...'.format(target))
            pass

def canary_bandwidth(db):
    now = time.time()
    try:
        bandwidth = probe_speedtest()
        cursor = db.cursor()
        cursor.execute('''
            INSERT INTO bandwidth_canary_results (time, down_speed, up_speed)
            VALUES (?, ?, ?)
        ''', [now, bandwidth[0], bandwidth[1]])
    except:
        log.warn('bandwidth canary failed...')
        pass

