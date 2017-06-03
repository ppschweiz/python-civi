# -*- coding: utf-8 -*-

import os
from pingen_api import Pingen

token = os.environ['PINGEN_TOKEN']
pingen = Pingen(token, staging=False)

def postal_mail_file(filename, dryrun):
	filestream = open(filename, 'rb')
	result = pingen.push_document(filename, filestream, send=(not dryrun), speed=2, color=1)
	status = result[2]['status']
	reqfail = result[2]['requirement_failure']
	address = result[2]['address'].replace('\n', ', ')
	sent = result[2]['sent']

	if status != 1:
		raise ValueError('Pingen API status is: ' + status)
		
	if reqfail != 0:
		raise ValueError('Ping requirement failed: ' + reqfail)

	if sent == 1:
		print("Letter mailed to " + address)
	else:
		print("Letter uploaded but not mailed to " + address)

