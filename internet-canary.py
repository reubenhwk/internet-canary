#!/usr/bin/env python3

from InternetCanary import canary
import time
import sys
import logging as log
import yaml

def STON(S):
    return (S * 1000 * 1000 * 1000)

def NTOU(N):
    return (N / 1000)

def NTOS(N):
    return (N / (1000 * 1000 * 1000))

def schedule(interval):
    now = time.time()
    last = int(now)
    last -= last % interval
    sleep_time = interval - (now - last)
    log.info('sleeping {} seconds...'.format(sleep_time))
    time.sleep(sleep_time)

if __name__ == '__main__':
    log.basicConfig(level=log.INFO)
    log.info('starting')

    config = yaml.load(open(sys.argv[1]).read())

    db = canary.setup_db(config['dbpath'])

    while True:
        log.info('running dns canary...')
        canary.canary_dns(db, config['dns_targets'])

        log.info('running http canary...')
        canary.canary_http(db, config['http_targets'])

        log.info('running bandwidth canary...')
        canary.canary_bandwidth(db)

        db.commit()

        schedule(300)
    
