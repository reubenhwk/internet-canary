#!/usr/bin/env python3

import InternetCanary
import time
import sys
import logging as log
import yaml

if __name__ == '__main__':
    log.basicConfig(level=log.INFO)
    log.info('starting')

    config = yaml.load(open(sys.argv[1]).read())

    db = InternetCanary.setup_db(config['dbpath'])

    while True:
        log.info('running http canary...')
        InternetCanary.http_canary(db, config['http_targets'])

        log.info('running bandwidth canary...')
        InternetCanary.bandwidth_canary(db)

        db.commit()

        log.info('sleeping 300 seconds...')
        time.sleep(300)
    
