#!/usr/bin/env python

from flask import Flask, render_template
import sqlite3
import time
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import StringIO

app = Flask(__name__)

@app.route("/")
def simple_hello():

    conn = sqlite3.connect('/var/lib/internet-canary/internet-canary.db')

    c = conn.cursor()

    targets = c.execute('''
        select distinct target from results order by target;
    ''').fetchall()

    end = time.time()
    start = end - 8000

    svgs=list()
    for target in targets:
        rows = c.execute('''
           select time, result from results
               where target = ? and time >= ? and time <= ?
               order by time;
        ''', (target[0], start, end)).fetchall()

        plt.plot(
            [row[0] for row in rows],
            [row[1] for row in rows],
        )
        plt.title(target[0])
        plt.ylabel('response time in seconds')
        plt.ylim(0,1)
        xmin = rows[0][0]
        xmax = rows[-1][0]
        plt.xlim(xmin, xmax)
        r = range(10)
        plt.xticks(
           [(xmax - xmin) * (x / 9.0) + xmin for x in r],
           [str(x) for x in r],
        )
        svg=StringIO.StringIO()
        plt.savefig(svg, format='svg')
        plt.close()
        svg.seek(0)
        svgs.append(svg.buf)

    return render_template('simple-hello.txt', svgs=svgs)
