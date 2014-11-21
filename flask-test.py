#!/usr/bin/python

from datetime import datetime
import time

from flask import Flask, jsonify, request
from flask import jsonify

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

GPIO.setup(17, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)

GPIO.output(17, True);
GPIO.output(22, True);



app = Flask(__name__ )

@app.route('/')
def index():
    return app.send_static_file('index.html')



@app.route('/hello')
def hello_world():
    return 'Hello world'


@app.route('/currentTime')
def currentTime():

    print "Hey.. I got called"
    return jsonify(
	{"date_time":str(datetime.now()),
	 "epoch":int(time.time())}
    )

@app.route('/off/<pin>')
def off(pin):
    GPIO.output(17, False)
    return jsonify(
       { pin : "0" }
    )

@app.route('/on/<pin>')
def on(pin):
    GPIO.output(17, True)
    return jsonify(
       { pin : "1" }
    )

@app.route('/pin/<int:pin>/<int:state>')
def on(pin, state):
    GPIO.output(pin, state)
    return jsonify(
       { pin : state }
    )

@app.route('/toggle/<int:pin>')
def toggle( pin ):
    GPIO.output(pin, not GPIO.input(pin))
    return jsonify(
       { pin : GPIO.input(pin) }
    )




if __name__ == '__main__':
    app.run( host = '0.0.0.0', debug=True )

