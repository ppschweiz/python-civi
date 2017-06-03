# -*- coding: utf-8 -*-
#
# Pirate Party Switzerland membership management script
# Created by Stefan Thoeni at 2015-12-5
#
# Assign member ids to new members
#

import datetime
import hashlib

def sha1(text):
	h = hashlib.sha1()
	h.update(text.encode('ascii'))
	return h.hexdigest()

def sha256(text):
	h = hashlib.sha256()
	h.update(text.encode('ascii'))
	return h.hexdigest()

def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def parse_datetime(datestring, default):
	if datestring == '':
		return default
	else:
		return datetime.datetime.strptime(datestring, '%Y-%m-%d %H:%M:%S');

def parse_date(datestring, default):
	if datestring == '':
		return default
	else:
		return datetime.datetime.strptime(datestring, '%Y-%m-%d');

def parse_int(intstring):
	if intstring == '':
		return 0
	else:
		return int(intstring)

def trim(text):
	return text.strip(' \n\t\r')

