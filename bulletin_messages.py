# -*- coding: utf-8 -*-
#
# Pirate Party Switzerland membership management script
# Created by Stefan Thoeni at 2017-06-02
#
# Create a bulletin message for a member
#

import sys
import os
import datetime
from string import Template
from util import trim
from util import sha1
from model import Person
from model import Membership
from sendemail import send_encrypted_email
from sendemail import notify_admin
from sendemail import format_address
from files import get_text

sender_de = format_address(u'PPS - Präsidium der Piratenversammlung', 'ppv@piratenpartei.ch')
sender_fr = format_address(u'PPS - Préidence de l\'Assemblée Pirate', 'ppv@piratenpartei.ch')
sender_it = format_address(u'PPS - Présidence de l\'Assemblée Pirate', 'ppv@piratenpartei.ch')
sender_en = format_address(u'PPS - Präsidium der Piratenversammlung', 'ppv@piratenpartei.ch')
registry = format_address(u'Piratenpartei Schweiz', 'ppv@piratenpartei.ch')
testbox = format_address(u'Stefan Thöni', 'stefan.thoeni@piratenpartei.ch')
senderkey = os.environ['SENDER_PGP_KEY']

def format_message(person, voteid, extension):
	text = get_text('bulletin', voteid + '/' + person.short_language(), 'invitation', extension)
	template = Template(text)
	return template.substitute(GREET=person.greeting)

def send_message(person, voteid, dryrun, pgpkey, attachement=None, attachementname=None):
	text = format_message(person, voteid, 'txt')
	html = format_message(person, voteid, 'html')
	subject = trim(format_message(person, voteid, 'subject'))
	
	if person.short_language() == 'fr':
		sender = sender_fr
	elif person.short_language() == "it":	
		sender = sender_it
	elif person.short_language() == "en":	
		sender = sender_en
	else:
		sender = sender_de

	encrypt_for = [senderkey, pgpkey]
	receipient = format_address(person.firstname + u' ' + person.lastname, person.email)
	if not dryrun:
		send_encrypted_email(receipient, registry, subject, html, text, attachement, attachementname, sign=senderkey, encrypt_for=[pgpkey,senderkey])
		send_encrypted_email(sender, receipient, subject, html, text, attachement, attachementname, sign=senderkey, encrypt_for=[pgpkey,senderkey])
	else:
		send_encrypted_email(receipient, testbox, subject, html, text, attachement, attachementname, sign=senderkey, encrypt_for=[pgpkey,senderkey])
		sys.stderr.write('Not sending mail due to dry run\n');

