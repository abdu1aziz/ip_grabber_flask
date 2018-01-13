#!/bin/bash/python27
# Author: Abdul Aziz
# GitHub: @abdu1aziz

from flask import Flask, jsonify, render_template, request
from urllib2 import urlopen
import re, json
import datetime, os


host = "192.168.1.245" # LAN IP
#host = "127.0.0.1"  # LOOPBACK ADDRESS
port = 80
logfile = 'tmp/ip_record.log'
os.remove(logfile)
open(logfile, 'a').close()

app = Flask(__name__)



def logg_client_info():
	now = datetime.datetime.now()
	now = str(now)
	now = now.split('.')[0]
	log_file = open(logfile, 'a+')
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
	log_file.close()

@app.route('/')
def home_page():
	global get_ip
	global get_isp
	global get_city
	global get_state
	global get_country

	get_ip = request.environ['REMOTE_ADDR']
	get_ip = str(get_ip)
	url = "http://ip-api.com/json/%s" % (get_ip)
	response = urlopen(url)
	data = json.load(response)
	get_isp = data['org']
	get_city = data['city']
	get_country = data['country']
	get_state = data['region']
	logg_client_info()
	return render_template('index.html', get_ip=get_ip, get_city=get_city, get_state=get_state, get_country=get_country, get_isp=get_isp)



if __name__ == '__main__':
	app.run(host=host, port=port)



# THE END
