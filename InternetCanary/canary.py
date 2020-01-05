#!/usr/bin/env python3

import pathlib
import requests
import speedtest
import sqlite3
import sys
import time
import dns.resolver

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
    try:
        r = requests.get(url, timeout=timeout)
        if r.status_code == requests.codes.ok:
            return r.elapsed.total_seconds()
    except:
        pass

    return -1

def setup_db(dbpath):

    path = pathlib.Path(dbpath)
    path.parent.mkdir(parents=True, exist_ok=True)

    db = sqlite3.connect(dbpath)
    cursor = db.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS http_canary_results (
            target text not null,
            time real not null,
            result real not null);
    ''')
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS target_time ON http_canary_results (target, time);
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bandwidth_canary_results (
            time real not null,
            down_speed integer not null,
            up_speed integer not null);
    ''')
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS bandwidth_time ON bandwidth_canary_results (time);
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS dns_canary_results (
            target text not null,
            time real not null,
            result real not null);
    ''')
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS dns_time ON dns_canary_results (time);
    ''')


    db.commit()

    return db

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
        except dns.resolver.NoNameservers:
            pass

def canary_http(db, targets):
    cursor = db.cursor()
    for target in targets:
        now = time.time()
        result = probe_http(target, 5)
        cursor.execute('''
           INSERT INTO http_canary_results (target, time, result)
           VALUES (?, ?, ?)
        ''', [target, now, result])

def canary_bandwidth(db):
    now = time.time()
    bandwidth = probe_speedtest()
    cursor = db.cursor()
    cursor.execute('''
        INSERT INTO bandwidth_canary_results (time, down_speed, up_speed)
        VALUES (?, ?, ?)
    ''', [now, bandwidth[0], bandwidth[1]])


