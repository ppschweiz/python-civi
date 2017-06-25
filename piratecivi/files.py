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
from .util import parse_datetime
from .util import trim
from .sendemail import notify_admin

TMP_DIR = '/tmp'

def get_content_dir(app):
	return TMP_DIR + '/' + app + '-content'

def get_not_after_file(app):
	return get_content_dir(app) + '/not-after'

def readfile(filename):
	with codecs.open(filename, 'r', encoding='utf-8') as fil:
		return fil.read()

def checkout_content(app):
	subprocess.check_call('./checkout-content.sh ' + app, shell=True)

def get_text(app, target, mode, extension):
	return readfile(get_content_dir(app) + '/' + target + '/' + mode + '.' + extension)

def check_not_after(app):
	text = readfile(get_not_after_file(app))
	date = parse_datetime(trim(text), datetime.datetime(2000, 1, 1))
	now = datetime.datetime.now()
	if now > date:
		sys.stderr.write('Factura content expired\n')
		notify_admin(u'Factura content expired', u'Factura content expired at {0}'.format(date))
		return False
	else:
		sys.stderr.write('Factura content valid\n')
		return True
