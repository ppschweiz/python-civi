# -*- coding: utf-8 -*-
#
# Pirate Party Switzerland membership management script
# Created by Stefan Thoeni at 2015-12-5
#
# Person entity (=member record)
#
# Special fields:
# * Verifikation für Televotia/Urabstimmung: custom_7
# * Rechnungsdatum: custom_17
# * Mahnungsdatum: custom_18
# * Zahlungsdatum: custom_19

import sys
import os
from pythoncivicrm.pythoncivicrm import CiviCRM
from pythoncivicrm.pythoncivicrm import CivicrmError
from pythoncivicrm.pythoncivicrm import matches_required
from util import is_number
from departments import get_departments
import datetime

def get_required_fields():
	return 'external_identifier,first_name,last_name,email,country,city,street_address,postal_code,phone,state_province,preferred_language,gender_id,custom_7,custom_17,custom_18,custom_19'

def parse_date(datestring):
	if datestring == '':
		return datetime.datetime(2000, 1, 1, 0, 0)
	else:
		return datetime.datetime.strptime(datestring, '%Y-%m-%d %H:%M:%S');

class Person:
	def __init__(self, civicrm, **kwargs):
		self.civicrm = civicrm

		if 'contact' in kwargs:
			contact = kwargs['contact']
		elif 'member_id' in kwargs:
			args = {}
			args['external_identifier'] = kwargs['member_id']
			args['return'] = get_required_fields()
			contact = civicrm.get('Contact', **args)[0]
		else:
			raise ValueError('now loading argument stated')
			
		self.civi_id = int(contact['id'])

		if is_number(contact['external_identifier']):
			self.member_id = int(contact['external_identifier'])
		else:
			self.member_id = 0

		self.firstname = contact['first_name']
		self.lastname = contact['last_name']
		self.email = contact['email']
		self.country = contact['country']
		self.city = contact['city']
		self.street = contact['street_address']
		self.postalcode = contact['postal_code']
		self.phone = contact['phone']
		self.state = contact['state_province_name']
		self.language = contact['preferred_language']
		self.gender  = contact['gender_id']

		if self.language == 'de_CH':
			if self.gender == '1':
				self.greeting = u'Liebe ' + self.firstname
			elif self.gender == '2':
				self.greeting = u'Lieber ' + self.firstname
			else:
				self.greeting = u'Hallo ' + self.firstname
		elif self.language == 'fr_FR':
			if self.gender == '1':
				self.greeting = u'Chère ' + self.firstname
			elif self.gender == '2':
				self.greeting = u'Cher ' + self.firstname
			else:
				self.greeting = u'Salut ' + self.firstname
		else:
			self.greeting = u'Hello ' + self.firstname

		if 'memberships' in kwargs:
			if kwargs['memberships'] != None:
				self.memberships = list();
				for membership in kwargs['memberships']:
					if membership.contact_id == self.civi_id:
						self.memberships.append(membership)
		else:
			self.memberships = list();
			membership_values = civicrm.get('Membership', contact_id=self.civi_id)
			for membership_data in membership_values:
				membership = Membership(data=membership_data)
				self.memberships.append(membership)

		self.section = type('Department', (), {})()
		self.section.number = 0
		self.section.fullname = ''
		self.section.parent = None
		self.section.amount = 0

		for membership in self.memberships:
			if membership.department.number > 2 and membership.department.amount > 0:
				self.section = membership.department

		self.verified = (contact['custom_7'] == '1')

		self.facturadate = parse_date(contact['custom_17'])
		self.reminderdate = parse_date(contact['custom_18'])
		self.paymentdate = parse_date(contact['custom_19'])

	def update_facturadate(self, date):
		self.facturadate = date
		self.civicrm.update('Contact', self.civi_id, custom_17=self.facturadate)

	def update_reminderdate(self, date):
		self.reminderdate = date
		self.civicrm.update('Contact', self.civi_id, custom_18=self.reminderdate)

class Membership:
	def __init__(self, **kwargs):
		if 'data' in kwargs:
			data = kwargs['data']
		else:
			raise ValueError('no data provided')

		self.contact_id = int(data['contact_id']);
		self.name = data['membership_name']

		deps = get_departments()

		if self.name in deps:
			self.department = deps[self.name]
		else:
			sys.stderr.write('Unknown department: ' + self.name + "\n")
			self.department = None

		if data['status_id'] == 2:
			self.active = True
		else:
			self.active = False

