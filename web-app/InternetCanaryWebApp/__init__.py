#!/usr/bin/env python

from flask import Flask, render_template
import sqlite3

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

    svgs=list()
    for target in targets:
	datapoints = 288
        # TODO: This selects the most recent points, but in the wrong order.
        rows = c.execute("select time, result from results where target = ? order by time desc limit ?;", (target[0], datapoints)).fetchall()
        plt.plot([rows[x][1] for x in xrange(len(rows))])
        plt.ylabel('response time')
        plt.ylim(0,1)
        plt.xlim(0,datapoints)
        plt.title(target[0])
        svg=StringIO.StringIO()
        plt.savefig(svg, format='svg')
        plt.close()
        svg.seek(0)
        svgs.append(svg.buf)

    rows = c.execute('''
        select time, result from results order by time desc limit 30;
    ''').fetchall()

    return render_template('simple-hello.txt', svgs=svgs)
