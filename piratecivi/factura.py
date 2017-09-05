# -*- coding: utf-8 -*-
#
# Pirate Party Switzerland membership management script
# Created by Stefan Thoeni at 2016-11-07
#
# Create a factura for a member
#

import sys
import os
import datetime
import subprocess
import hashlib
from string import Template
from time import sleep
from pythoncivicrm.pythoncivicrm import CiviCRM
from pythoncivicrm.pythoncivicrm import CivicrmError
from pythoncivicrm.pythoncivicrm import matches_required
from .util import parse_datetime
from .util import trim
from .model import Person
from .model import Membership
from .sendemail import notify_admin
from .factura_messages import send_message
from .files import get_text

site_key = os.environ['CIVI_SITE_KEY']
api_key = os.environ['CIVI_API_KEY']
url = os.environ['CIVI_API_URL'] 
civicrm = CiviCRM(url, site_key, api_key, True)

def get_factura_ref(person, year):
	return u'10000{:06d}{:04d}0'.format(person.member_id, year)

def get_factura_number(person, year):
	return u'{:04d}{:06d}'.format(year, person.member_id)

def get_section_amount(person):
	if person.section.amount > 0:
		return str(person.section.amount) + '.00'
	else:
		return ''

def get_total_amount(person):
	return str(person.section.amount + 80) + '.00'

def format_date(language, date):
	if language == 'de':
		return u'{}. {} {:04d}'.format(date.day, date.strftime('%B'), date.year)
	elif language == 'fr':
		return u'{} {} {:04d}'.format(date.day, date.strftime('%B'), date.year)
	else:
		return u'{:04d}-{:02d}-{:02d}'.format(date.year, date.month, date.day)

def create_factura(person, date, slip):
	subprocess.check_call('./prepare.sh factura', shell=True)
	
	if (date.month == 12) or (date.month == 11):
		year = date.year + 1
	else:
		year = date.year

	country = person.country;
	if country == 'Schweiz' or country == 'Suisse':
		country = 'Switzerland'

	csv = open("/tmp/factura/people.csv", "w")
	csv.write(u'{};{};{};{};{};{};{};{};{};{};{};{};{};{};{};{};{};{}'.format(
		person.member_id, 
		person.lastname, 
		person.firstname, 
		person.email, 
		country, 
		person.street, 
		person.postalcode, 
		person.city, 
		person.greeting, 
		person.section.fullname, 
		get_section_amount(person), 
		get_total_amount(person), 
		get_factura_number(person, year), 
		get_factura_number(person, year), 
		get_factura_ref(person, year), 
		format_date(person.short_language(), date), year,
		'yes' if slip else 'no'))
	csv.close()

	subprocess.check_call('./compile.sh factura ' + person.short_language(), shell=True)

def make_factura(person, date):
	create_factura(person, date, False)
	os.rename('/tmp/factura/factura.pdf', 'Rechnung.pdf')

def send_factura(person, date, reminderlevel, dryrun):
	create_factura(person, date, True)
	
	if reminderlevel == 0:
		mode = 'bill'
	elif reminderlevel == 1:
		mode = 'reminder'
	elif reminderlevel == 2:
		mode = 'reminder2'
	else:
		mode = 'reminder3'
	
	if person.short_language() == 'fr':
		attachmentname = 'facture.pdf'
	elif person.short_language() == 'it':	
		attachmentname = 'facture.pdf'
	elif person.short_language() == 'en':	
		attachmentname = 'bill.pdf'
	else:
		attachmentname = 'Rechnung.pdf'

	send_message(person, mode, dryrun, '/tmp/factura/factura.pdf', attachmentname)

def handle_member(person, dryrun):
	now = datetime.datetime.now()
	if (now > (person.facturadate + datetime.timedelta(days=365))) and (person.paymentdate > now + datetime.timedelta(days=-30)):
		sys.stderr.write('Member {} has payed before factura\n'.format(person.member_id))
		
		if not dryrun:
			facdate = person.paymentdate + datetime.timedelta(days=-1)
			person.update_factura(facdate, facdate, 0)
		else:
			sys.stderr.write('Not updating factura in dry run\n')

		return 1

	if (now > (person.facturadate + datetime.timedelta(days=365))) and (now > (person.joindate + datetime.timedelta(hours=23))):
		sys.stderr.write('Member {} needs new factura\n'.format(person.member_id))
		send_factura(person, now, 0, dryrun)

		if not dryrun:
			person.update_factura(now, now, 0)
		else:
			sys.stderr.write('Not updating factura in dry run\n')

		return 1

	elif (person.facturadate > person.paymentdate) and (now > (person.reminderdate + datetime.timedelta(days=30))) and (now < (person.facturadate + datetime.timedelta(days=110))) and (person.reminderlevel < 3):
		sys.stderr.write('Member {} needs new reminder\n'.format(person.member_id))
		send_factura(person, person.facturadate, person.reminderlevel + 1, dryrun)

		if not dryrun:
			person.update_reminder(now, person.reminderlevel + 1)
		else:
			sys.stderr.write('Not updating reminder in dry run\n');

		return 1

	else:
		return 0

def update_idserverstatus(person, dryrun):
	if person.isppsmember and person.idserverstatus == 0:
		if dryrun:
			sys.stderr.write('Not updating id server status for {} due to dry run\n'.format(person.member_id));
		else:
			person.update_idserverstatus(1)
			sys.stderr.write('Activated server status for {}\n'.format(person.member_id));

def update_membership(person, dryrun):
	now = datetime.datetime.now()
	#has payed current factura => shold be active
	if (person.facturadate >= (now + datetime.timedelta(days=-1095))) and (person.paymentdate >= person.facturadate):
		if not person.ppsmembership.active:
			if not dryrun:
				person.update_memberships(True, person.paymentdate, person.facturadate + datetime.timedelta(days=425))
				sys.stderr.write('Activated already payed memberships for person id {}\n'.format(person.member_id))
			else:
				sys.stderr.write('Not activating already payed memberships for person id {} in dryrun\n'.format(person.member_id))

	# payment in the last year and current factura not yet 60 days old => should be active
	elif (person.paymentdate >= person.facturadate + datetime.timedelta(days=-365)) and (now < person.facturadate + datetime.timedelta(days=60)):
		if not person.ppsmembership.active:
			if not dryrun:
				person.update_memberships(True, person.paymentdate, person.facturadate + datetime.timedelta(days=60))
				sys.stderr.write('Activated not yet expired memberships for person id {}\n'.format(person.member_id))
			else:
				sys.stderr.write('Not activating not yet expired memberships for person id {}\n'.format(person.member_id))

	# other cases => should be inactive
	else:
		if person.ppsmembership.active:
			if not dryrun:
				person.update_memberships(False, person.paymentdate, person.facturadate + datetime.timedelta(days=60))
				sys.stderr.write('Deactivated epxired memberships for person id {}\n'.format(person.member_id))
			else:
				sys.stderr.write('Not deactivating epxired memberships for person id {} in dryrun\n'.format(person.member_id))

