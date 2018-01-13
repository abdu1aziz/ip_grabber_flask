#!/bin/bash/python27

from flask import Flask, jsonify, render_template, request
from urllib2 import urlopen
import re, json
import datetime, os
import os.path

__author__ = 'Abdul Aziz'
host = "192.168.1.245"                 # LAN IP
#host = "127.0.0.1"                   # LOOPBACK ADDRESS
port = 80                            # Port where flask page will be running on.
logfile = 'tmp/ip_record.log'       # Log File Name and Path.

def log_data_check():
	if os.path.isfile(logfile):    # Check if log file already exists?
		os.remove(logfile)        # IF Does Remove it to make a new file.
	open(logfile, 'a').close()   # Create a new Log File.
log_data_check()


app = Flask(__author__)



def logg_client_info():
	now = datetime.datetime.now()             # Logging Date And Time Alongside.
	now = str(now)							  # Change Date & Time to string.
	now = now.split('.')[0]                   # Formatting Snipping Date & Time.
	log_file = open(logfile, 'a+')            # Opening Log File And Logging Data.
	log_file.write("""
-------------------------------------
|   VISITOR'S LOGGED INFORMATION    |
-------------------------------------
| DATE/TIME :  %s  |
-------------------------------------
| GITHUB: @abdu1aziz -- Abdul Aziz  |
-------------------------------------
| IP ADDRESS: %s        |
-------------------------------------
| I.S.P     :  %s         |
-------------------------------------
| CITY      :  %s            |
-------------------------------------
| STATE     :  %s                   |
-------------------------------------
| COUNTRY   :  %s          |
-------------------------------------
\n
	""" % (str(now), get_ip, str(get_isp), get_city, get_state, get_country))
	log_file.close()                          # Closing File After Loggin Data.

@app.route('/')
def home_page():
	"""Making Variables below Global;
	   So They Can Be accessed from a
	   Different function."""
	global get_ip
	global get_isp
	global get_city
	global get_state
	global get_country

	get_ip = request.environ['REMOTE_ADDR']         # Getting Remote IP ADDRESS.
	get_ip = str(get_ip)                            # Converting IP ADDRESS To A String.
	url = "http://ip-api.com/json/%s" % (get_ip)    # Attaching IP ADDRESS TO URL.
	response = urlopen(url)                         # OPENING URL.
	data = json.load(response)                      # LOADING DATA TO JSON.
	get_isp = data['org']                           # DECLARING VARIABLES FROM JSON.
	get_city = data['city']
	get_country = data['country']
	get_state = data['region']
	logg_client_info()                              # INITIALIZING LOGGING FUNCTION TO LOG DATA UPON EVERY PAGE REFRESH.
	return render_template('index.html', get_ip=get_ip, get_city=get_city, get_state=get_state, get_country=get_country, get_isp=get_isp)



if __author__ == 'Abdul Aziz':
	app.run(host=host, port=port)                    # RUNNING THE PROGRAM!



# THE END
