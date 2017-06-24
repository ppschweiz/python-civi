# -*- coding: utf-8 -*-
#
# Pirate Party Switzerland membership management script
# Created by Stefan Thoeni at 2017-06-02
#
# Send mail migration message
#

import sys
import os
import re
from string import Template
from pythoncivicrm.pythoncivicrm import CiviCRM
from pythoncivicrm.pythoncivicrm import CivicrmError
from pythoncivicrm.pythoncivicrm import matches_required
from util import trim
from model import Person
from sendemail import notify_admin
from mail_migrate_messages import send_message

bulletin_secret = os.environ['BULLETIN_SECRET'] 
site_key = os.environ['CIVI_SITE_KEY']
api_key = os.environ['CIVI_API_KEY']
url = os.environ['CIVI_API_URL'] 
civicrm = CiviCRM(url, site_key, api_key, True)

def send_migration(person, event, dryrun):

	pp_mail = None
	alt_mail = None
	
	for email in person.emails:
		if email.email.endswith('@piratenpartei.ch'):
			pp_mail = email.email
		elif email.email.endswith('@partipirate.ch'):
			pp_mail = email.email
		elif email.email.endswith('@partitopirata.ch'):
			pp_mail = email.email
		elif email.email.endswith('@pirateparty.ch'):
			pp_mail = email.email
		else:
			alt_mail = email.email

	if pp_mail != None and ('.' in pp_mail.split('@')[0]):
		if person.isppsmember:
			if alt_mail != None:
				send_message(person, event, 'altmail', alt_mail, pp_mail, alt_mail, dryrun)
				send_message(person, event, 'altmail', pp_mail, pp_mail, alt_mail, dryrun)
				return 1
			else:
				send_message(person, event, 'noaltmail', pp_mail, pp_mail, alt_mail, dryrun)
				return 1
		else:
			send_message(person, event, 'nonmember', pp_mail, pp_mail, alt_mail, dryrun)
			return 1
	else:
		return 0



