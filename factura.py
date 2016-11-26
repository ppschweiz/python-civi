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
from sendemail import send_email
from sendemail import notify_admin
from time import sleep

site_key = os.environ['CIVI_SITE_KEY']
api_key = os.environ['CIVI_API_KEY']
url = os.environ['CIVI_API_URL'] 
paylink_base = os.environ['PAYLINK_BASE'] 
paylink_secret = os.environ['PAYLINK_SECRET'] 
civicrm = CiviCRM(url, site_key, api_key, True)
sender_de = u'"Piratenpartei Schweiz" <info@piratenpartei.ch>'
sender_fr = u'"Parti Pirate Suisse" <info@partipirate.ch>'
registry = u'"Piratenpartei Schweiz" <registrar@piratenpartei.ch>'

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
	if language == 'de_CH':
		return u'{}. {} {:04d}'.format(date.day, date.strftime('%B'), date.year)
	elif language == 'fr_FR':
		return u'{} {} {:04d}'.format(date.day, date.strftime('%B'), date.year)
	else:
		return u'{:04d}-{:02d}-{:02d}'.format(date.year, date.month, date.day)

def sha1(text):
	h = hashlib.sha1()
	h.update(text)
	return h.hexdigest()

def build_paylink(person):
	return paylink_base + "/pay#" + sha1(paylink_secret + ":paylink/" + str(person.member_id))[:20] + "/" + str(person.member_id)

def format_message(person, date, filename):
	 with open(filename, "rb") as fil:
		text = fil.read()
		template = Template(text)
		return template.substitute(GREET=person.greeting, PAYURL=build_paylink(person))

def create_factura(person, date, reminderlevel):
	if (date.month == 12) or (date.month == 11):
		year = date.year + 1
	else:
		year = date.year

	csv = open("people.csv", "w")
	csv.write(u'{};{};{};{};{};{};{};{};{};{};{};{};{};{};{};{};{}'.format(person.member_id, person.lastname, person.firstname, person.email, person.country, person.street, person.postalcode, person.city, person.greeting, person.section.fullname, get_section_amount(person), get_total_amount(person), get_factura_number(person, year), get_factura_number(person, year), get_factura_ref(person, year), format_date(person.language, date), year).encode('utf8'))
	csv.close()

	if person.language == 'fr_FR':
		language = 'fr'
	if person.language == "it_IT":	
		language = 'fr'
	else:
		language = 'de'

	if reminderlevel == 0:
		mode = 'bill'
	elif reminderlevel == 1:
		mode = 'reminder'
	elif reminderlevel == 2:
		mode = 'reminder2'
	else:
		mode = 'reminder3'

	subprocess.check_call('./compile.sh ' + language + ' ' + mode, shell=True)

def send_factura(person, date, reminderlevel, dryrun):
	create_factura(person, date, reminderlevel)

	text = format_message(person, date, 'tmp/msg.txt')
	html = format_message(person, date, 'tmp/msg.html')
	subject = trim(format_message(person, date, 'tmp/msg.subject'))
	
	if person.language == 'fr_FR':
		attachmentname = "facture.pdf"
		sender = sender_fr
	if person.language == "it_IT":	
		attachmentname = "facture.pdf"
		sender = sender_fr
	else:
		attachmentname = "Rechnung.pdf"
		sender = sender_de

	receipient = (u'"' + person.firstname + u' ' + person.lastname + u'" <' + person.email + u'>')

	send_email(sender, registry, subject, html, text, 'tmp/factura.pdf', attachmentname)
	if not dryrun:
		send_email(sender, receipient, subject, html, text, 'tmp/factura.pdf', attachmentname)
	else:
		print('Not sending mail due to dry run');

def handle_member(person, dryrun):
	now = datetime.datetime.now()
	if now > (person.facturadate + datetime.timedelta(days=365)):
		print('Member {} needs new factura'.format(person.member_id))
		send_factura(person, now, 0, dryrun)

		if not dryrun:
			person.update_factura(now, now, 0)
		else:
			print('Not updating factura in dry run');

		sleep(60)

	elif ((person.facturadate > person.paymentdate) and  now > (person.reminderdate + datetime.timedelta(days=30))) and (now < (person.facturadate + datetime.timedelta(days=110))):	
		print('Member {} needs new reminder'.format(person.member_id))
		send_factura(person, person.facturadate, person.reminderlevel + 1, dryrun)

		if not dryrun:
			person.update_reminder(now, person.reminderlevel + 1)
		else:
			print('Not updating reminder in dry run');

		sleep(60)

def update_membership(person, dryrun):
	now = datetime.datetime.now()
	#has pay current factura => shold be active
	if person.paymentdate >= person.facturadate:
		if not person.ppsmembership.active:
			if not dryrun:
				person.update_memberships(True, person.paymentdate, person.facturadate + datetime.timedelta(days=425))
				print('Activated already payed memberships for person id ' + str(person.member_id))
			else:
				print('Not activating already payed memberships for person id ' + str(person.member_id) + ' in dryrun')

	# payment in the last year and current factura not yet 60 days old => should be active
	elif (person.paymentdate >= person.facturadate + datetime.timedelta(days=-365)) and (now < person.facturadate + datetime.timedelta(days=60)):
		if not person.ppsmembership.active:
			if not dryrun:
				person.update_memberships(True, person.paymentdate, person.facturadate + datetime.timedelta(days=60))
				print('Activated not yet expired memberships for person id ' + str(person.member_id))
			else:
				print('Not activating not yet expired memberships for person id ' + str(person.member_id) + ' in dryrun')

	# other cases => should be inactive
	else:
		if person.ppsmembership.active:
			if not dryrun:
				person.update_memberships(False, person.paymentdate, person.facturadate + datetime.timedelta(days=60))
				print('Deactivated epxired memberships for person id ' + str(person.member_id))
			else:
				print('Not deactivating epxired memberships for person id ' + str(person.member_id) + ' in dryrun')


def check_not_after():
	subprocess.check_call('./not-after.sh', shell=True)
	with open('not-after', "rb") as fil:
		date = parse_datetime(trim(fil.read()), datetime.datetime(2000, 1, 1))
	subprocess.call('rm not-after', shell=True)
	now = datetime.datetime.now()
	if now > date:
		notify_admin(u'Factura content expired', u'Factura content expired at {0}'.format(date))
		return False
	else:
		return True
