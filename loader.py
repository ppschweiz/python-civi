# -*- coding: utf-8 -*-
#
# Pirate Party Switzerland membership management script
# Created by Stefan Thoeni at 2015-12-5
#
# Assign member ids to new members
#

import sys
import os
from pythoncivicrm.pythoncivicrm import CiviCRM
from pythoncivicrm.pythoncivicrm import CivicrmError
from pythoncivicrm.pythoncivicrm import matches_required
from model import Person
from model import Membership
from model import Email
from model import get_required_fields_person

site_key = os.environ['CIVI_SITE_KEY']
api_key = os.environ['CIVI_API_KEY']
url = os.environ['CIVI_API_URL'] 
civicrm = CiviCRM(url, site_key, api_key, True)

def load(civicrm, entity_type, **kwargs):

	report = ('progress' in kwargs) and (kwargs['progress'] == 1)
	if report:
		sys.stderr.write('Downloading ' + entity_type + '...\n')
	
	if 'memberships' in kwargs:
		memberships = kwargs['memberships']
	else:
		memberships = None
	
	if 'emails' in kwargs:
		emails = kwargs['emails']
	else:
		emails = None

	if 'batch' in kwargs:
		batch = int(kwargs['batch'])
	else:
		batch = 10

	allfilter = dict()
	for key in kwargs:
		if key != 'memberships' and key != 'emails' and key != 'batch' and key != 'progress' and key != 'verification':
			allfilter[key] = kwargs[key]

	count = civicrm.getcount(entity_type, **allfilter)
	entities = list()

	while len(entities) < count:

		batchfilter = dict()
		batchfilter['limit']=batch
		batchfilter['offset']=len(entities)
		for key in kwargs:
			if key == 'returnfields':
				batchfilter['return'] = kwargs[key]
			if key != 'memberships' and key != 'emails':
				batchfilter[key] = kwargs[key]

		download = civicrm.get(entity_type, **batchfilter)

		if 'verification' in kwargs:
			verification = kwargs['verification']
		else:
			verification = False

		for data in download:
			if entity_type == 'Contact':
				entities.append(Person(civicrm, contact=data, verification=verification, memberships=memberships, emails=emails))
			elif entity_type == 'Membership':
				entities.append(Membership(civicrm, data=data))
			elif entity_type == 'Email':
				entities.append(Email(civicrm, data=data))
			else:
				raise ValueError('unknown entity type')

		if report:
			sys.stderr.write('Got ' + str(len(entities)) + ' of ' + str(count) + ' ' + entity_type + "\n");

	if report:
		sys.stderr.write('Got all ' + str(len(entities)) + ' ' + entity_type + "\n")

	return entities

def load_emails(civicrm, **kwargs):
	return load(civicrm, 'Email', **kwargs)

def load_memberships(civicrm, **kwargs):
	return load(civicrm, 'Membership', **kwargs)

def load_persons(civicrm, **kwargs):
	return load(civicrm, 'Contact', **kwargs)

def load_all(civicrm, progress, batch, verification=False):
	emails = load_emails(civicrm, progress=progress, batch=batch*2)
	memberships = load_memberships(civicrm, progress=progress, batch=batch/2*3)
	return load_persons(civicrm, progress=progress, batch=batch, verification=verification, memberships=memberships, emails=emails, returnfields=get_required_fields_person())

