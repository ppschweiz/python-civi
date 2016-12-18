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
import hashlib
from string import Template
from util import trim
from model import Person
from model import Membership
from sendemail import send_email
from sendemail import notify_admin
from files import get_text

paylink_base = os.environ['PAYLINK_BASE'] 
paylink_secret = os.environ['PAYLINK_SECRET'] 
sender_de = u'"Piratenpartei Schweiz" <info@piratenpartei.ch>'
sender_fr = u'"Parti Pirate Suisse" <info@partipirate.ch>'
sender_it = u'"Partito Pirate Svizzera" <info@partitopirata.ch>'
sender_en = u'"Pirate Party Switzerland" <info@pirateparty.ch>'
registry = u'"Piratenpartei Schweiz" <registrar@piratenpartei.ch>'

def sha1(text):
	h = hashlib.sha1()
	h.update(text)
	return h.hexdigest()

def build_paylink(person):
	return paylink_base + u'/pay#' + sha1(paylink_secret + u':paylink/' + str(person.member_id))[:20] + "/" + str(person.member_id)

def format_message(person, mode, extension):
	text = get_text(person.short_language(), mode, extension)
	template = Template(text)
	return template.substitute(GREET=person.greeting, PAYURL=build_paylink(person))

def send_message(person, mode, dryrun, attachement=None, attachementname=None):
	text = format_message(person, mode, 'txt')
	html = format_message(person, mode, 'html')
	subject = trim(format_message(person, mode, 'subject'))
	
	if person.short_language() == 'fr':
		sender = sender_fr
	elif person.short_language() == "it":	
		sender = sender_it
	elif person.short_language() == "en":	
		sender = sender_en
	else:
		sender = sender_de

	receipient = (u'"' + person.firstname + u' ' + person.lastname + u'" <' + person.email + u'>')
	send_email(sender, registry, subject, html, text, attachement, attachementname)
	if not dryrun:
		send_email(sender, receipient, subject, html, text, attachement, attachementname)
	else:
		print('Not sending mail due to dry run');

