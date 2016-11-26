# -*- coding: utf-8 -*-
#
# Pirate Party Switzerland membership management script
# Created by Stefan Thoeni at 2016-11-07
#
# Create factures for members
#

import sys
import os
from pythoncivicrm.pythoncivicrm import CiviCRM
from pythoncivicrm.pythoncivicrm import CivicrmError
from pythoncivicrm.pythoncivicrm import matches_required
from loader import load_all
from factura import handle_member
from factura import check_not_after
from sendemail import notify_admin
from memberids import assign_member_ids
from factura import update_membership

site_key = os.environ['CIVI_SITE_KEY']
api_key = os.environ['CIVI_API_KEY']
url = os.environ['CIVI_API_URL'] 
civicrm = CiviCRM(url, site_key, api_key, True)

def update_memberships(members, dryrun):
	for member in members:
		if member.isppsmember:
			try:
				update_membership(member, dryrun)
			except Exception as e:
				msg = u'MemberId: {}\n{}\n{}'.format(member.member_id, type(e), e)
				print(msg)
				notify_admin(u'Error in update_membership', msg)

def process_facturas(dryrun):
	try:
		members = load_all(civicrm, 1, 200)
		assign_member_ids(members, dryrun)
	
		if check_not_after():
			for member in members:
				if member.isppsmember:
					try:
						handle_member(member, dryrun)
					except Exception as e:
						msg = u'MemberId: {}\n{}\n{}'.format(member.member_id, type(e), e)
						print(msg)
						notify_admin(u'Error in handle_member', msg)

		update_memberships(members, dryrun)

	except Exception as e:
		msg = u'{}\n{}'.format(type(e), e)
		print(msg)
		notify_admin(u'Error in process_factura', msg)


