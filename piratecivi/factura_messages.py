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
from .util import trim
from .util import sha1
from .model import Person
from .model import Membership
from .sendemail import send_signed_email
from .sendemail import send_encrypted_email
from .sendemail import notify_admin
from .sendemail import format_address
from .files import get_text

paylink_base = os.environ['PAYLINK_BASE'] 
paylink_secret = os.environ['PAYLINK_SECRET'] 
sender_de = format_address(u'Piratenpartei Schweiz', 'info@piratenpartei.ch')
sender_fr = format_address(u'Parti Pirate Suisse', 'info@partipirate.ch')
sender_it = format_address(u'Partito Pirate Svizzera', 'info@partitopirata.ch')
sender_en = format_address(u'Pirate Party Switzerland', 'info@pirateparty.ch')
registry = format_address(u'Piratenpartei Schweiz', 'registrar@piratenpartei.ch')
testbox = format_address(os.environ['TESTBOX_NAME'], os.environ['TESTBOX_MAIL'])
senderkey = os.environ['SENDER_PGP_KEY']

def build_paylink(person):
	return paylink_base + u'/pay#' + sha1(paylink_secret + u':paylink/' + str(person.member_id))[:20] + "/" + str(person.member_id)

def format_message(person, mode, extension):
	text = get_text('factura', person.short_language(), mode, extension)
	template = Template(text)
	return template.substitute(GREET=person.greeting, PAYURL=build_paylink(person))

def send_message(person, mode, dryrun, attachement=None, attachementname=None, pgpkey=None):
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

	receipient = format_address(person.firstname + u' ' + person.lastname, person.email)
	if not dryrun:
		if pgpkey == None:
			send_signed_email(sender, receipient, subject, html, text, senderkey, attachement, attachementname, registry)
		else:
			send_encrypted_email(sender, receipient, subject, html, text, attachement, attachementname, sign=senderkey, encrypt_for=[pgpkey,senderkey])
	else:
		if pgpkey == None:
			send_signed_email(receipient, testbox, subject, html, text, senderkey, attachement, attachementname)
		else:
			send_encrypted_email(receipient, testbox, subject, html, text, attachement, attachementname, sign=senderkey, encrypt_for=[pgpkey,senderkey])
		sys.stderr.write('Not sending mail due to dry run\n');

