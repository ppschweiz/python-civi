# -*- coding: utf-8 -*-
#
# Pirate Party Switzerland membership management script
# Created by Stefan Thoeni at 2016-11-07
#
# Create factures for members
#

import sys
import os
import subprocess
from pythoncivicrm.pythoncivicrm import CiviCRM
from pythoncivicrm.pythoncivicrm import CivicrmError
from pythoncivicrm.pythoncivicrm import matches_required
from loader import load_all
from bulletin import send_bulletin
from files import check_not_after
from files import checkout_content
from sendemail import notify_admin
from factura import update_membership
from errors import handle_error

site_key = os.environ['CIVI_SITE_KEY']
api_key = os.environ['CIVI_API_KEY']
url = os.environ['CIVI_API_URL'] 
export_gpg_dir = '/tmp/gpgkeys'
civicrm = CiviCRM(url, site_key, api_key, True)

def update_memberships(members, dryrun):
	sys.stderr.write('Updating memberships\n')
	for member in members:
		if member.isppsmember:
			try:
				update_membership(member, dryrun)
			except Exception as e:
				handle_error(e, 'MemberId: ' + str(member.member_id))

def update_pgpkeys(members):
	sys.stderr.write('Updating OpenPGP keys\n')
	if not os.path.isdir(export_gpg_dir):
		os.makedirs(export_gpg_dir)
	for member in members:
		if member.openpgp_attachement_id > 0:
			member.load_openpgp_keydata()
			keyfile = open(os.path.join(export_gpg_dir, str(member.member_id) + '.asc'), 'w')
			keyfile.write(member.openpgp_keydata)
			keyfile.close()
	subprocess.check_call('./import_gpg.sh ' + export_gpg_dir, shell=True)

def process_bulletins(voteid, postal, dryrun):
	try:
		checkout_content('bulletin')

		members = load_all(civicrm, 1, 200)
		update_memberships(members, dryrun)
		update_pgpkeys(members)

		if check_not_after('bulletin'):
			sys.stderr.write('Sending bulletin to all verified members...\n')
			counter = 0
			for member in members:
				if member.isppsmember and member.verified:
					try:
						send_bulletin(member, voteid, postal, dryrun)
						counter = counter + 1
					except Exception as e:
						handle_error(e, 'MemberId: ' + str(member.member_id))
			sys.stderr.write('{0} bulletins sent.\n'.format(counter))


	except Exception as e:
		handle_error(e)


