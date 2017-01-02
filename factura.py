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
from pythoncivicrm.pythoncivicrm import CiviCRM
from pythoncivicrm.pythoncivicrm import CivicrmError
from pythoncivicrm.pythoncivicrm import matches_required
from util import parse_datetime
from util import trim
from model import Person
from model import Membership
from sendemail import notify_admin
from messages import send_message
from time import sleep
from files import get_text

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

def create_factura(person, date):
	subprocess.check_call('./prepare.sh', shell=True)
	
	if (date.month == 12) or (date.month == 11):
		year = date.year + 1
	else:
		year = date.year

	csv = open("/tmp/factura/people.csv", "w")
	csv.write(u'{};{};{};{};{};{};{};{};{};{};{};{};{};{};{};{};{}'.format(person.member_id, person.lastname, person.firstname, person.email, person.country, person.street, person.postalcode, person.city, person.greeting, person.section.fullname, get_section_amount(person), get_total_amount(person), get_factura_number(person, year), get_factura_number(person, year), get_factura_ref(person, year), format_date(person.short_language(), date), year).encode('utf8'))
	csv.close()

	subprocess.check_call('./compile.sh ' + person.short_language(), shell=True)

def send_factura(person, date, reminderlevel, dryrun):
	create_factura(person, date)
	
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
	if person.short_language() == 'it':	
		attachmentname = 'facture.pdf'
	if person.short_language() == 'en':	
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

	if (now > (person.facturadate + datetime.timedelta(days=365))) and (now > (person.joindate + datetime.timedelta(hours=23))):
		sys.stderr.write('Member {} needs new factura\n'.format(person.member_id))
		send_factura(person, now, 0, dryrun)

		if not dryrun:
			person.update_factura(now, now, 0)
		else:
			sys.stderr.write('Not updating factura in dry run\n')

		sleep(60)

	elif ((person.facturadate > person.paymentdate) and  now > (person.reminderdate + datetime.timedelta(days=30))) and (now < (person.facturadate + datetime.timedelta(days=110))):	
		sys.stderr.write('Member {} needs new reminder\n'.format(person.member_id))
		send_factura(person, person.facturadate, person.reminderlevel + 1, dryrun)

		if not dryrun:
			person.update_reminder(now, person.reminderlevel + 1)
		else:
			sys.stderr.write('Not updating reminder in dry run\n');

		sleep(60)

def update_membership(person, dryrun):
	now = datetime.datetime.now()
	#has pay current factura => shold be active
	if person.paymentdate >= person.facturadate:
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

