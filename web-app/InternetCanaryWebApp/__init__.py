#!/usr/bin/env python

from flask import Flask, render_template
import sqlite3
import time
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import StringIO

app = Flask(__name__)

def epoch_to_human(t):
    return time.strftime('%I:%M%p', time.localtime(t))

def interpolate(xmin, xmax, ratio):
    return (xmax - xmin) * ratio + xmin

@app.route("/")
def simple_hello():

    conn = sqlite3.connect('/var/lib/internet-canary/internet-canary.db')

    c = conn.cursor()

    targets = c.execute('''
        select distinct target from results order by target;
    ''').fetchall()

    now = time.time()
    end = now
    start = now - 60 * 60 * 4

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
        r = range(7)
        xticks = [interpolate(xmin, xmax, x / float(len(r)-1)) for x in r]
        plt.xticks(
           xticks,
           [epoch_to_human(x) for x in xticks],
           rotation = -45,
           ha='left'
        )
        plt.tight_layout()
        plt.grid(True, linestyle='--')
        svg=StringIO.StringIO()
        plt.savefig(svg, format='svg')
        plt.close()
        svg.seek(0)
        svgs.append(svg.buf)

    return render_template('simple-hello.txt', svgs=svgs)
