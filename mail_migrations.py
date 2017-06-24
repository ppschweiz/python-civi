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
from mail_migrate import send_migration
from files import check_not_after
from files import checkout_content
from sendemail import notify_admin
from factura import update_membership
from errors import handle_error

site_key = os.environ['CIVI_SITE_KEY']
api_key = os.environ['CIVI_API_KEY']
url = os.environ['CIVI_API_URL']
civicrm = CiviCRM(url, site_key, api_key, True)

def process_migrations(event, dryrun):
	try:
		checkout_content('mailmigration')

		members = load_all(civicrm, 1, 200)

		if check_not_after('mailmigration'):
			sys.stderr.write('Notification about mail migration...\n')
			counter = 0
			for member in members:
				try:
					counter += send_migration(member, event, dryrun)
				except Exception as e:
					handle_error(e, 'MemberId: ' + str(member.member_id))
			sys.stderr.write('{0} migration infos sent.\n'.format(counter))
	except Exception as e:
		handle_error(e)


