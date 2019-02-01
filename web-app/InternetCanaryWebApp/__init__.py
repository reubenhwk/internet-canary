#!/usr/bin/env python

from datetime import datetime
from flask import Flask, render_template
import sqlite3

import PyGnuplot as gplot

app = Flask(__name__)

@app.route("/")
def simple_hello():

    conn = sqlite3.connect('/var/lib/internet-canary/internet-canary.db')

    c = conn.cursor()

    rows = c.execute('''
        select time, result from results order by time desc limit 30;
    ''').fetchall()

    targets = c.execute('''
        select distinct target from results;
    ''').fetchall()

    return render_template('simple-hello.txt', targets=targets, rows=rows, date=str(datetime.now()))
