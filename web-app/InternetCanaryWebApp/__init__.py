#!/usr/bin/env python

from flask import Flask, render_template, request
import sqlite3
import time
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import StringIO

app = Flask(__name__)

conn = sqlite3.connect('/var/lib/internet-canary/internet-canary.db')

def epoch_to_human(t):
    return time.strftime('%m/%d/%y\n%I:%M%p', time.localtime(t))

def interpolate(xmin, xmax, ratio):
    return (xmax - xmin) * ratio + xmin

@app.route("/")
def index():
    return '''
    <html>
       <ul>
         <li><a href='http://35.160.69.193/rt'>rt</a></li>
         <li><a href='http://35.160.69.193/bw'>bw</a></li>
       </ul>
    </html>
    '''

@app.route("/rt")
def reponse_time_page():

    try:
        start = int(request.form['start'])
        end = int(request.form['end'])
    except:
        now = time.time()
        start = now - 60 * 60 * 24
        end = now

    c = conn.cursor()

    targets = c.execute('''
        select distinct target from results order by target;
    ''').fetchall()

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
        plt.ylim(0, 3)
        xmin = start
        xmax = end
        plt.xlim(xmin, xmax)
        r = range(7)
        xticks = [interpolate(xmin, xmax, x / float(len(r)-1)) for x in r]
        plt.xticks(
           xticks,
           [epoch_to_human(x) for x in xticks]
        )
        plt.tight_layout()
        plt.grid(True, linestyle='--')
        svg=StringIO.StringIO()
        plt.savefig(svg, format='svg')
        plt.close()
        svg.seek(0)
        svgs.append(svg.buf)

    return render_template('rt.txt', svgs=svgs)

@app.route("/bw")
def bandwidth_page():

    try:
        start = int(request.form['start'])
        end = int(request.form['end'])
    except:
        now = time.time()
        start = now - 60 * 60 * 4
        end = now

    c = conn.cursor()

    rows = c.execute('''
       select time, up_speed, down_speed from bandwidth_results
           where time >= ? and time <= ?
           order by time;
    ''', (start, end)).fetchall()

    plt.plot(
        [row[0] for row in rows],
        [row[1]/1000**2 for row in rows],
    )
    plt.plot(
        [row[0] for row in rows],
        [row[2]/1000**2 for row in rows],
    )
    plt.title('speedtest')
    plt.ylabel('Mbps')
    xmin = start
    xmax = end
    plt.xlim(xmin, xmax)
    r = range(7)
    xticks = [interpolate(xmin, xmax, x / float(len(r)-1)) for x in r]
    plt.xticks(
       xticks,
       [epoch_to_human(x) for x in xticks]
    )
    plt.tight_layout()
    plt.grid(True, linestyle='--')
    svg=StringIO.StringIO()
    plt.savefig(svg, format='svg')
    plt.close()
    svg.seek(0)

    return render_template('bw.txt', svg=svg.buf)
