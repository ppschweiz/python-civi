# -*- coding: utf-8 -*-

import sys
import os
from .pingen_api import Pingen

token = os.environ['PINGEN_TOKEN']
pingen = Pingen(token, staging=False)

def postal_mail_file(filename, dryrun, speed):
	filestream = open(filename, 'rb')
	result = pingen.push_document(filename, filestream, send=(not dryrun), speed=speed, color=1)
	status = result[2]['status']
	reqfail = result[2]['requirement_failure']
	address = result[2]['address'].replace('\n', ', ')
	sent = result[2]['sent']

	if status != 1:
		raise ValueError(u'Pingen API status is: {}'.format(status))
		
	if reqfail != 0:
		raise ValueError(u'Ping requirement failed: {}'.format(reqfail))

	if dryrun:
		sys.stderr.write(u'Letter uploaded but not mailed to {}\n'.format(address))
	else:
		sys.stderr.write(u'Letter mailed to {}\n'.format(address))

