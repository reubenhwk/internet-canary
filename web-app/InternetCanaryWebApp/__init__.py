#!/usr/bin/env python

from datetime import datetime
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def simple_hello():
    return render_template('simple-hello.txt', date=str(datetime.now()))
