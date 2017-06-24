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
from string import Template
from util import trim
from util import sha1
from model import Person
from model import Membership
from sendemail import send_email
from sendemail import notify_admin
from sendemail import format_address
from files import get_text

sender_de = format_address(u'Piratenpartei Schweiz', 'info@piratenpartei.ch')
sender_fr = format_address(u'Parti Pirate Suisse', 'info@partipirate.ch')
sender_it = format_address(u'Partito Pirate Svizzera', 'info@partitopirata.ch')
sender_en = format_address(u'Pirate Party Switzerland', 'info@pirateparty.ch')
registry = format_address(u'Piratenpartei Schweiz', 'registrar@piratenpartei.ch')
testbox = format_address(u'Stefan Thöni', 'stefan.thoeni@piratenpartei.ch')

def format_message(person, event, info, extension, ppmail, altmail):
	text = get_text('mailmigration', event + '/' + person.short_language(), info, extension)
	template = Template(text)
	return template.substitute(GREET=person.greeting, PPMAIL=ppmail, ALTMAIL=altmail)

def send_message(person, event, info, email, ppmail, altmail, dryrun):
	text = format_message(person, event, info, 'txt', ppmail, altmail)
	html = format_message(person, event, info, 'html', ppmail, altmail)
	subject = trim(format_message(person, event, info, 'subject', ppmail, altmail))
	
	if person.short_language() == 'fr':
		sender = sender_fr
	elif person.short_language() == "it":	
		sender = sender_it
	elif person.short_language() == "en":	
		sender = sender_en
	else:
		sender = sender_de

	if person.lastname != '':
		receipient = format_address(person.firstname + u' ' + person.lastname, email)
	else:
		receipient = email

	if not dryrun:
		send_email(receipient, registry, subject, html, text)
		send_email(sender, receipient, subject, html, text)
	else:
		send_email(receipient, testbox, subject, html, text)
		sys.stderr.write('Not sending mail due to dry run\n');

