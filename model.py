# -*- coding: utf-8 -*-
#
# Pirate Party Switzerland membership management script
# Created by Stefan Thoeni at 2015-12-5
#
# Assign member ids to new members
#

import sys
import os
from pythoncivicrm.pythoncivicrm import CiviCRM
from pythoncivicrm.pythoncivicrm import CivicrmError
from pythoncivicrm.pythoncivicrm import matches_required
from util import is_number
from departments import get_departments

class Person:
	def __init__(self, civicrm, **kwargs):
		self.civicrm = civicrm

		if 'contact' in kwargs:
			contact = kwargs['contact']
		elif 'member_id' in kwargs:
			contact = civicrm.get('Contact', external_identifier=kwargs['member_id'])[0]
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

		if 'verification' in kwargs and kwargs['verification'] == True:
			self.verified = False
			verification_values = civicrm.get('CustomValue', entity_id=self.civi_id)
			for verification_data in verification_values:
				if verification_data['id'] == '7' and verification_data['0'] == '1':
					self.verified = True

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

