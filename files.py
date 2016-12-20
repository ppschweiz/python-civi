# -*- coding: utf-8 -*-
#
# Pirate Party Switzerland membership management script
# Created by Stefan Thoeni at 2016-11-07
#
# Create a factura for a member
#

import sys
import os
import subprocess
import datetime
import codecs
from util import parse_datetime
from util import trim
from sendemail import notify_admin

TMP_DIR = '/tmp'
CONTENT_DIR = TMP_DIR + '/factura-content'
NOT_AFTER_FILE = CONTENT_DIR + '/not-after'

def readfile(filename):
	with codecs.open(filename, 'r', encoding='utf-8') as fil:
		return fil.read()

def checkout_content():
	subprocess.check_call('./checkout-content.sh', shell=True)

def get_text(language, mode, extension):
	return readfile(CONTENT_DIR + '/' + language + '/' + mode + '.' + extension)

def check_not_after():
	text = readfile(NOT_AFTER_FILE)
	date = parse_datetime(trim(text), datetime.datetime(2000, 1, 1))
	now = datetime.datetime.now()
	if now > date:
		print('Factura content expired')
		notify_admin(u'Factura content expired', u'Factura content expired at {0}'.format(date))
		return False
	else:
		print('Factura content valid')
		return True
