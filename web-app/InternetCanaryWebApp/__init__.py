#!/usr/bin/env python

from datetime import datetime
from flask import Flask, render_template
import sqlite3

import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt

app = Flask(__name__)

@app.route("/")
def simple_hello():

    conn = sqlite3.connect('/var/lib/internet-canary/internet-canary.db')

    c = conn.cursor()

    targets = c.execute('''
        select distinct target from results;
    ''').fetchall()

    i = 0
    for target in targets:
        rows = c.execute("select time, result from results where target = ? order by time desc limit 120;", target).fetchall()
        plt.plot([rows[x][1] for x in xrange(len(rows))])
        plt.ylabel('response time')
        plt.title(target)
        plt.savefig('/tmp/{}.svg'.format(i))
        plt.close()
        i += 1

    rows = c.execute('''
        select time, result from results order by time desc limit 30;
    ''').fetchall()

    return render_template('simple-hello.txt', targets=targets, rows=rows, date=str(datetime.now()))
