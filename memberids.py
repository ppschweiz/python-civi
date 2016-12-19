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
from loader import load_all
from updater import update_entity
from messages import send_message
from sendemail import notify_admin

def assign_member_ids(members, dryrun):
	#run through all contacts and determine the current highest member id
	print('Determining highest current member id...');
	high_member_id = 0
	for member in members:
		print('Hightest ' + str(high_member_id) + ', this: '+ str(member.member_id))
		if member.member_id > high_member_id:
			high_member_id = member.member_id

	print('Highest assigned member id is currently ' + str(high_member_id))

	#run through all contacts and assign new member ids where necessary
	print('Assigning new member ids...');
	for member in members:
		if len(member.memberships) > 0 and member.member_id < 1:
			high_member_id = high_member_id + 1
			member.member_id = str(high_member_id)
			if not dryrun:
				update_entity(civicrm, 'Contact', str(member.civi_id), external_identifier=str(member.member_id))
				print('Assiging member id ' + str(member.member_id) + ' to contact ' + str(member.civi_id))
			else:
				print('Not assiging member id ' + str(member.member_id) + ' to contact ' + str(member.civi_id) + ' in dryrun')

			send_message(member, 'welcome', dryrun)

	print('Highest assigned member id is currently ' + str(high_member_id))

