# -*- coding: utf-8 -*-
#
# Pirate Party Switzerland membership management script
# Created by Stefan Thoeni at 2017-06-02
#
# Create a bulletin for a member
#

import sys
import os
import datetime
import subprocess
import re
import gnupg
from string import Template
from pythoncivicrm.pythoncivicrm import CiviCRM
from pythoncivicrm.pythoncivicrm import CivicrmError
from pythoncivicrm.pythoncivicrm import matches_required
from util import parse_datetime
from util import trim
from util import sha256
from model import Person
from model import Membership
from sendemail import notify_admin
from bulletin_messages import send_message
from time import sleep
from files import get_text
from pingen import postal_mail_file

bulletin_secret = os.environ['BULLETIN_SECRET'] 
site_key = os.environ['CIVI_SITE_KEY']
api_key = os.environ['CIVI_API_KEY']
url = os.environ['CIVI_API_URL'] 
civicrm = CiviCRM(url, site_key, api_key, True)
gpg = gnupg.GPG()
address = re.compile('^.*\ <(.*)\>$')

def get_keyid(receipient):
	keys = gpg.list_keys(False)
	for key in keys:
		if key['trust'] in ['u', 'f']:
			for uid in key['uids']:
				match = address.match(uid)
				if receipient == match.group(1):
					return key['keyid']
	return None

def format_date(language, date):
	if language == 'de':
		return u'{}. {} {:04d}'.format(date.day, date.strftime('%B'), date.year)
	elif language == 'fr':
		return u'{} {} {:04d}'.format(date.day, date.strftime('%B'), date.year)
	else:
		return u'{:04d}-{:02d}-{:02d}'.format(date.year, date.month, date.day)

def create_bulletin(person, voteid):
	subprocess.check_call('./prepare.sh bulletin', shell=True)

	security_code = sha256(bulletin_secret + str(person.member_id))
	
	csv = open("/tmp/bulletin/people.csv", "w")
	csv.write(u'{};{};{};{};{};{};{};{};{};{}'.format(person.member_id, 
													  person.lastname, 
													  person.firstname, 
													  person.email, 
													  person.country, 
													  person.street, 
													  person.postalcode, 
													  person.city, 
													  person.greeting,
													  security_code))
	csv.close()

	subprocess.check_call('./compile.sh bulletin ' + voteid + '/' + person.short_language(), shell=True)

def make_bulletin(person, voteid):
	create_bulletin(person, voteid)
	os.rename('/tmp/bulletin/bulletin.pdf', 'Bulletin.pdf')

def send_bulletin(person, voteid, dryrun):
	create_bulletin(person, voteid)
		
	if person.short_language() == 'fr':
		attachmentname = 'Abstimmung.pdf'
	if person.short_language() == 'it':	
		attachmentname = 'Votation.pdf'
	if person.short_language() == 'en':	
		attachmentname = 'Voting.pdf'
	else:
		attachmentname = 'Abstimmung.pdf'

	keyid = get_keyid(person.email)
	if keyid != None:
		print(u'Key for {} email {} found: {}'.format(person.member_id, person.email, keyid))
		send_message(person, voteid, dryrun, keyid, '/tmp/bulletin/bulletin.pdf', attachmentname)
	else:
		print(u'No key for {} email {}'. format(person.member_id, person.email))
		postal_mail_file('/tmp/bulletin/bulletin.pdf', dryrun)


