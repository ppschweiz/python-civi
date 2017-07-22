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
import gnupg
from string import Template
from pythoncivicrm.pythoncivicrm import CiviCRM
from pythoncivicrm.pythoncivicrm import CivicrmError
from pythoncivicrm.pythoncivicrm import matches_required
from .util import trim
from .model import Person
from .sendemail import notify_admin
from .mail_migrate_messages import send_message

bulletin_secret = os.environ['BULLETIN_SECRET'] 
site_key = os.environ['CIVI_SITE_KEY']
api_key = os.environ['CIVI_API_KEY']
url = os.environ['CIVI_API_URL'] 
civicrm = CiviCRM(url, site_key, api_key, True)
gpg = gnupg.GPG()
address = re.compile('^.*\ <(.*)\>$')

def get_password(passwords, ppmail):
	if ppmail.endswith('@partipirate.ch'):
		ppmail = ppmail.replace('@partipirate.ch', '@piratenpartei.ch')
	if ppmail.endswith('@partitopirata.ch'):
		ppmail = ppmail.replace('@partitopirata.ch', '@piratenpartei.ch')
	if ppmail in passwords:
		return passwords[ppmail]
	else:
		return None

def get_keyid(receipient):
	keys = gpg.list_keys(False)
	for key in keys:
		if key['trust'] in ['u', 'f']:
			for uid in key['uids']:
				match = address.match(uid)
				if receipient == match.group(1):
					return key['keyid']
	return None

def send_migration(person, event, passwords, dryrun):

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
		keyid = get_keyid(person.email)
		password = get_password(passwords, pp_mail)

		if (passwords == None) or (password != None):
			if keyid != None:
				sys.stderr.write(u'Key for {} email {} found: {}\n'.format(person.member_id, person.email, keyid))
			else:
				sys.stderr.write(u'No key for {} email {}\n'.format(person.member_id, person.email))

			if person.isppsmember:
				if alt_mail != None:
					send_message(person, event, 'altmail', alt_mail, pp_mail, alt_mail, password, keyid, dryrun)
					if passwords == None:
						send_message(person, event, 'altmail', pp_mail, pp_mail, alt_mail, None, None, dryrun)
					return 1
				elif passwords == None:
					send_message(person, event, 'noaltmail', pp_mail, pp_mail, alt_mail, None, None, dryrun)
					return 1
				else:
					return 0
			else:
				send_message(person, event, 'nonmember', pp_mail, pp_mail, alt_mail, password, keyid, dryrun)
				return 1
		else:
			sys.stderr.write(u'No password for {} email {}\n'.format(person.member_id, person.email))
			return 0
	else:
		return 0



