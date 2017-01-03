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

def assign_member_ids(civicrm, members, dryrun):
	#run through all contacts and determine the current highest member id
	sys.stderr.write('Determining highest current member id...\n');
	high_member_id = 0
	for member in members:
		if member.member_id > high_member_id:
			high_member_id = member.member_id

	sys.stderr.write('Highest assigned member id before updates is \n'.format(high_member_id))

	#run through all contacts and assign new member ids where necessary
	sys.stderr.write('Assigning new member ids...\n');
	for member in members:
		if len(member.memberships) > 0 and member.member_id < 1:
			high_member_id = high_member_id + 1
			member.member_id = str(high_member_id)
			if not dryrun:
				update_entity(civicrm, 'Contact', str(member.civi_id), external_identifier=str(member.member_id))
				sys.stderr.write('Assiging member id {} to contact {}\n'.format(member.member_id, member.civi_id))
			else:
				sys.stderr.write('Not assiging member id {} to contact {} in dryrun\n'.format(member.member_id, member.civi_id))

			send_message(member, 'welcome', dryrun)

	sys.stderr.write('Highest assigned member id after updates is {}\n'.format(high_member_id))

