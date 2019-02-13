#!/usr/bin/env python3

from flask import Flask, render_template, request, url_for
import sqlite3
import time
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import io
import yaml

app = Flask(__name__)

config = yaml.load(open('/etc/internet-canary.d/internet-canary.yaml').read())
def getdb():
    return sqlite3.connect(config['dbpath'])

def epoch_to_human(t):
    return time.strftime('%m/%d/%y\n%I:%M%p', time.localtime(t))

def interpolate(xmin, xmax, ratio):
    return (xmax - xmin) * ratio + xmin

def default_time_range():
    try:
        start = int(request.args.get('start'))
        end = int(request.args.get('end'))
    except:
        now = time.time()
        start = now - 60 * 60 * 24
        end = now

    return start, end

@app.route("/")
def index():
    return '''
    <html>
       <ul>
         <li><a href='{}'>bw</a></li>
         <li><a href='{}'>dns</a></li>
         <li><a href='{}'>rt</a></li>
       </ul>
    </html>
    '''.format(
        url_for('bandwidth_page'),
        url_for('dns_reponse_time_page'),
        url_for('http_response_time_page')
    )

@app.route("/dns/svg")
def dnssvg(target=None, start=None, end=None):

    try:
        if target == None:
            target = request.args.get('target')

        if start == None:
            start = int(request.args.get('start'))

        if end == None:
            end = int(request.args.get('end'))
    except:
        return ":)"

    conn = getdb()
    c = conn.cursor()

    rows = c.execute('''
       select time, result from dns_canary_results
           where target = ? and time >= ? and time <= ?
           order by time;
    ''', (target, start, end)).fetchall()

    plt.plot(
        [row[0] for row in rows],
        [row[1] for row in rows],
    )

    plt.title(target)
    plt.ylabel('response time in seconds')
    plt.ylim(0, 1)

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
    svg=io.StringIO()
    plt.savefig(svg, format='svg')
    plt.close()
    svg.seek(0)

    return svg.getvalue()

@app.route("/dns")
def dns_reponse_time_page():

    start, end = default_time_range()

    return render_template(
        'rt.txt',
        svgs=[
            dnssvg(target, start, end) for target in config['dns_targets']
        ]
    )

@app.route("/rt/svg")
def rtsvg(target=None, start=None, end=None):

    try:
        if target == None:
            target = request.args.get('target')

        if start == None:
            start = int(request.args.get('start'))

        if end == None:
            end = int(request.args.get('end'))
    except:
        return ":)"

    conn = getdb()
    c = conn.cursor()

    rows = c.execute('''
       select time, result from http_canary_results
           where target = ? and time >= ? and time <= ?
           order by time;
    ''', (target, start, end)).fetchall()

    plt.plot(
        [row[0] for row in rows],
        [row[1] for row in rows],
    )

    plt.title(target)
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
    svg=io.StringIO()
    plt.savefig(svg, format='svg')
    plt.close()
    svg.seek(0)

    return svg.getvalue()

@app.route("/rt/last_x_minute/<int:minutes>")
def http_response_time_last_x_minutes(minutes=1):
    end = time.time()
    start = end - minutes * 60
    return render_template(
        'rt.txt',
        svgs=[
            rtsvg(target, start, end) for target in config['http_targets']
        ]
    )

@app.route("/rt/last_x_hours/<int:hours>")
def http_response_time_last_x_hours(hours=1):
    return http_response_time_last_x_minutes(hours * 60)

@app.route("/rt/last_x_days/<int:days>")
def http_response_time_last_x_days(days=1):
    return http_response_time_last_x_hours(days * 24)

@app.route("/rt/last_x_weeks/<int:weeks>")
def http_response_time_last_x_weeks(weeks=1):
    return http_response_time_last_x_days(weeks * 7)

@app.route("/rt")
def http_response_time_page():

    start, end = default_time_range()

    return render_template(
        'rt.txt',
        svgs=[
            rtsvg(target, start, end) for target in config['http_targets']
        ]
    )

@app.route("/bw/svg")
def bwsvg(start=None, end=None):

    try:
        if start == None:
            start = int(request.args.get('start'))

        if end == None:
            end = int(request.args.get('end'))
    except:
        return ":)"

    conn = getdb()
    c = conn.cursor()

    rows = c.execute('''
       select time, up_speed, down_speed from bandwidth_canary_results
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
    svg=io.StringIO()
    plt.savefig(svg, format='svg')
    plt.close()
    svg.seek(0)

    return svg.getvalue()

@app.route("/bw/last_x_minute/<int:minutes>")
def bandwidth_page_last_x_minutes(minutes=1):
    now = time.time()
    svg = bwsvg(now - minutes * 60, now)
    return render_template('bw.txt', svg=svg)

@app.route("/bw/last_x_hours/<int:hours>")
def bandwidth_page_last_x_hours(hours=1):
    return bandwidth_page_last_x_minutes(hours * 60)

@app.route("/bw/last_x_days/<int:days>")
def bandwidth_page_last_x_days(days=1):
    return bandwidth_page_last_x_hours(days * 24)

@app.route("/bw/last_x_weeks/<int:weeks>")
def bandwidth_page_last_x_weeks(weeks=1):
    return bandwidth_page_last_x_days(weeks * 7)

@app.route("/bw")
def bandwidth_page():

    start, end = default_time_range()

    svg = bwsvg(start, end)

    return render_template('bw.txt', svg=svg)
