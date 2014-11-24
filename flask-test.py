#!/usr/bin/python

import thread

from datetime import datetime
import time

from flask import Flask, jsonify, request
from flask import jsonify

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

GPIO.setup( 4, GPIO.OUT)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)

GPIO.output( 4, False);
GPIO.output(17, False);
GPIO.output(21, False);
GPIO.output(22, False);
GPIO.output(18, False);
GPIO.output(23, False);



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
    return return_status()

@app.route('/off/<pin>')
def off(pin):
    GPIO.output(pin, False)
    return return_status()

@app.route('/on/<pin>')
def on(pin):
    GPIO.output(pin, True)
    return return_status()

@app.route('/onwithdelay/<int:pin>/<int:delay>')
def onwithdelay(pin, delay):
    thread.start_new_thread(thread_on_with_delay, (pin, delay))
    return "Thread Started"

@app.route('/pin/<int:pin>/<int:state>')
def on(pin, state):
    GPIO.output(pin, state)
    return return_status()

@app.route('/toggle/<int:pin>')
def toggle( pin ):
    GPIO.output(pin, not GPIO.input(pin))
    return return_status()

@app.route('/level/<int:percent>')
def level( percent ):
    number = int(10*float(float(percent)/100))-1
    GPIO.output( 4, int('{0:08b}'.format(number)[7]))
    GPIO.output(17, int('{0:08b}'.format(number)[6]))
    GPIO.output(21, int('{0:08b}'.format(number)[5]))
    GPIO.output(22, int('{0:08b}'.format(number)[4]))

    return str(percent)+"%"
       

@app.route('/status')
def return_status():
    return jsonify(
        {
            4 : GPIO.input(4),
            17 : GPIO.input(17),
            21 : GPIO.input(21),
            22 : GPIO.input(22),
            18 : GPIO.input(18),
            23 : GPIO.input(23),
            "date_time":str(datetime.now()),
            "epoch":int(time.time())
        }
	
    )

def thread_on_with_delay(pin, delay):
    GPIO.output(pin, True)
    time.sleep(delay)
    GPIO.output(pin, False)


if __name__ == '__main__':
    app.run( host = '0.0.0.0', debug=True )

