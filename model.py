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
# * Mahnstufe: custom_20

import sys
import os
from pythoncivicrm.pythoncivicrm import CiviCRM
from pythoncivicrm.pythoncivicrm import CivicrmError
from pythoncivicrm.pythoncivicrm import matches_required
from util import is_number
from util import parse_datetime
from util import parse_date
from util import parse_int
from departments import get_departments
import datetime
from updater import update_entity

def get_required_fields_person():
	return 'contact_id,external_identifier,first_name,last_name,email,country,city,street_address,postal_code,phone,state_province,preferred_language,gender_id,custom_7,custom_17,custom_18,custom_19,custom_20'

class Person:
	def __init__(self, civicrm, **kwargs):
		self.civicrm = civicrm

		if 'contact' in kwargs:
			contact = kwargs['contact']
		elif 'member_id' in kwargs:
			args = {}
			args['external_identifier'] = kwargs['member_id']
			args['return'] = get_required_fields_person()
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
			args = {}
			args['contact_id'] = self.civi_id
			membership_values = civicrm.get('Membership', **args)
			for membership_data in membership_values:
				membership = Membership(civicrm, data=membership_data)
				self.memberships.append(membership)

		self.section = type('Department', (), {})()
		self.section.number = 0
		self.section.fullname = ''
		self.section.parent = None
		self.section.amount = 0
		self.isppsmember = False
		self.ppsmembership = None
		self.joindate = None

		for membership in self.memberships:
			if membership.department.number == 2:
				self.isppsmember = True
				self.ppsmembership = membership
				self.joindate = membership.joindate
			if membership.department.number > 2 and membership.department.amount > 0:
				self.section = membership.department

		self.verified = (contact['custom_7'] == '1')

		self.facturadate = parse_datetime(contact['custom_17'], datetime.datetime(2000, 1, 1))
		self.reminderdate = parse_datetime(contact['custom_18'], datetime.datetime(2000, 1, 1))
		self.paymentdate = parse_datetime(contact['custom_19'], datetime.datetime(2000, 1, 1))
		self.reminderlevel = parse_int(contact['custom_20'])

	def short_language(self):
		if self.language == 'fr_FR':
			return 'fr'
		elif self.language == "it_IT":	
			return 'it'
		elif self.language == "en_UK":	
			return 'en'
		else:
			return 'de'

	def update_paymentdate(self, date):
		self.paymentdate = date
		update_entity(self.civicrm, 'Contact', self.civi_id, custom_19=self.paymentdate)

	def update_facturadate(self, date):
		self.facturadate = date
		update_entity(self.civicrm, 'Contact', self.civi_id, custom_17=self.facturadate)

	def update_reminderdate(self, date):
		self.reminderdate = date
		update_entity(self.civicrm, 'Contact', self.civi_id, custom_18=self.reminderdate)

	def update_reminderlevel(self, level):
		self.reminderlevel = level
		update_entity(self.civicrm, 'Contact', self.civi_id, custom_20=self.reminderlevel)	
	def update_factura(self, facturadate, reminderdate, reminderlevel):
		self.facturadate = facturadate
		self.reminderdate = reminderdate
		self.reminderlevel = reminderlevel
		update_entity(self.civicrm, 'Contact', self.civi_id, custom_17=self.facturadate, custom_18=self.reminderdate, custom_20=self.reminderlevel)

	def update_reminder(self, reminderdate, reminderlevel):
		self.reminderdate = reminderdate
		self.reminderlevel = reminderlevel
		update_entity(self.civicrm, 'Contact', self.civi_id, custom_18=self.reminderdate, custom_20=self.reminderlevel)

	def update_memberships(self, active, start, end):
		for membership in self.memberships:
			membership.update(active, start, end)

#
# Membership 'PPZS', id=2
# 
# Membership status_id:
# - Pirate (bezahlt): 2
# - Mitglied (nicht bezahlt): 4
#

class Membership:
	def __init__(self, civicrm, **kwargs):
		if 'data' in kwargs:
			data = kwargs['data']
		else:
			raise ValueError('no data provided')

		self.civicrm = civicrm
		self.civi_id = int(data['id']);
		self.contact_id = int(data['contact_id']);
		self.name = data['membership_name']
		self.joindate = parse_date(data['join_date'], datetime.datetime(1990, 1, 1))
		self.active = (data['status_id'] == '2')

		deps = get_departments()

		if self.name in deps:
			self.department = deps[self.name]
		else:
			sys.stderr.write('Unknown department: ' + self.name + "\n")
			self.department = None

	def update(self, setactive, start, end):
		self.active = setactive

		if self.active:
			status = '2'
		else:
			status = '4'

		update_entity(self.civicrm, 'Membership', self.civi_id, is_override='1', status_id=status, start_date=start, end_date=end) 

