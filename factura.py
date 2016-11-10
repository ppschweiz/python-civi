# -*- coding: utf-8 -*-
#
# Pirate Party Switzerland membership management script
# Created by Stefan Thoeni at 2016-11-07
#
# Create factures for members
#

import sys
import os
from pythoncivicrm.pythoncivicrm import CiviCRM
from pythoncivicrm.pythoncivicrm import CivicrmError
from pythoncivicrm.pythoncivicrm import matches_required
import datetime
from model import Person
from model import Membership
from util import parse_date
from util import trim
from string import Template
from sendemail import send_email
from sendemail import notify_admin
import subprocess

site_key = os.environ['CIVI_SITE_KEY']
api_key = os.environ['CIVI_API_KEY']
url = os.environ['CIVI_API_URL'] 
civicrm = CiviCRM(url, site_key, api_key, True)

def get_factura_ref(person, date):
	return u'10000{:06d}{:04d}0'.format(person.member_id, date.year)

def get_factura_number(person, date):
	return u'{:04d}{:06d}'.format(date.year, person.member_id)

def get_section_amount(person):
	if person.section.amount > 0:
		return str(person.section.amount) + '.00'
	else:
		return ''

def get_total_amount(person):
	return str(person.section.amount + 80) + '.00'

def format_date(language, date):
	if language == 'de_CH':
		return u'{}. {} {:04d}'.format(date.day, date.strftime('%B'), date.year)
	elif language == 'fr_FR':
		return u'{} {} {:04d}'.format(date.day, date.strftime('%B'), date.year)
	else:
		return u'{:04d}-{:02d}-{:02d}'.format(date.year, date.month, date.day)

def format_message(person, date, filename):
	 with open(filename, "rb") as fil:
		text = fil.read()
		template = Template(text)
		return template.substitute(GREET=person.greeting)

def create_factura(person, date, remind):
	csv = open("people.csv", "w")
	csv.write(u'{};{};{};{};{};{};{};{};{};{};{};{};{};{};{};{};{}'.format(person.member_id, person.lastname, person.firstname, person.email, person.country, person.street, person.postalcode, person.city, person.greeting, person.section.fullname, get_section_amount(person), get_total_amount(person), get_factura_number(person, date), get_factura_number(person, date), get_factura_ref(person, date), format_date(person.language, date), date.year).encode('utf8'))
	csv.close()

	if person.language == 'fr_FR':
		language = 'fr'
	if person.language == "it_IT":	
		language = 'fr'
	else:
		language = 'de'

	if remind:
		mode = 'reminder'
	else:
		mode = 'bill'

	subprocess.call('./compile.sh ' + language + ' ' + mode, shell=True)

def send_factura(person, date, remind, dryrun):
	create_factura(person, date, remind)

	text = format_message(person, date, 'tmp/msg.txt')
	html = format_message(person, date, 'tmp/msg.html')
	subject = trim(format_message(person, date, 'tmp/msg.subject'))
	
	if person.language == 'fr_FR':
		attachmentname = "facture.pdf"
	if person.language == "it_IT":	
		attachmentname = "facture.pdf"
	else:
		attachmentname = "Rechnung.pdf"

	if not dryrun:
		send_email('info@piratenpartei.ch', person.email, subject, html, text, 'tmp/factura.pdf', attachmentname)

def handle_member(person, dryrun):
	now = datetime.datetime.now()
	if now > (person.facturadate + datetime.timedelta(days=365)):
		print(u'Member {} needs new factura'.format(person.member_id))
		send_factura(person, now, False, dryrun)

		if not dryrun:
			person.update_facturadate(now)
			person.update_reminderdate(now)

	elif ((person.facturadate > person.paymentdate) and  now > (person.reminderdate + datetime.timedelta(days=30))) and (now < (person.facturadate + datetime.timedelta(days=110))):	
		print(u'Member {} needs new reminder'.format(person.member_id))
		send_factura(person, person.facturadate, True, dryrun)

		if not dryrun:
			person.update_reminderdate(now)

def check_not_after():
	subprocess.call('./not-after.sh', shell=True)
	with open('not-after', "rb") as fil:
		date = parse_date(trim(fil.read()))
	subprocess.call('rm not-after', shell=True)
	now = datetime.datetime.now()
	if now > date:
		notify_admin(u'Factura content expired', u'Factura content expired at {0}'.format(date))
		return False
	else:
		return True
