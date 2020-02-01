#!/usr/bin/env python3

from InternetCanary import canary
import time
import sys
import logging as log
import yaml

def schedule(interval):
    now = time.time()
    wake_time = now + interval - now % interval
    sleep_duration = wake_time - now

    log.info('sleeping {} seconds...'.format(sleep_duration))
    time.sleep(sleep_duration)

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
    
