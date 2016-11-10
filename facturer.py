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

site_key = os.environ['CIVI_SITE_KEY']
api_key = os.environ['CIVI_API_KEY']
url = os.environ['CIVI_API_URL'] 
civicrm = CiviCRM(url, site_key, api_key, True)

try:
	if check_not_after():
		members = load_all(civicrm, 1, 200)

		for member in members:
			if member.isppsmember:
				try:
					handle_member(member, True)
				except Exception as e:
					msg = u'{}\n{}\n{}\n{}'.format(member.member_id, type(e), e.args, e)
					print(msg)
					notify_admin(u'Error in factura', msg)
except Exception as e:
	msg = u'{}\n{}\n{}'.format(type(e), e.args, e)
	print(msg)
	notify_admin(u'Error in factura', msg)
