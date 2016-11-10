# -*- coding: utf-8 -*-
#
# Pirate Party Switzerland membership management script
# Created by Stefan Thoeni at 2015-12-5
#
# Assign member ids to new members
#

import datetime

def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def parse_date(datestring):
	if datestring == '':
		return datetime.datetime(2000, 1, 1, 0, 0)
	else:
		return datetime.datetime.strptime(datestring, '%Y-%m-%d %H:%M:%S');

def trim(text):
	return text.strip(' \n\t\r')

