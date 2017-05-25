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
from loader import load_persons
from model import get_required_fields_person

reload(sys)
sys.setdefaultencoding('utf-8')

site_key = os.environ['CIVI_SITE_KEY']
api_key = os.environ['CIVI_API_KEY']
url = os.environ['CIVI_API_URL'] 
civicrm = CiviCRM(url, site_key, api_key, True)

reset_filename = sys.argv[1]
export_gpg_dir = sys.argv[2]

def load_memberlist():
	with open(sys.argv[2]) as f:
		memberidlist = f.read().splitlines()
	memberlist = list();
	for member_id in memberidlist:
		onemember = load_persons(civicrm, external_identifier=member_id, progress=1, batch=20, returnfields=get_required_fields_person())
		for member in onemember:
			memberlist.append(member)
	return memberlist

def load_allmembers():
	allmembers = load_all(civicrm, 1, 200, True)
	memberlist = list();
	for member in allmembers:
		if member.isppsmember and member.idserverstatus >= 1:
			memberlist.append(member)
	return memberlist

members = load_allmembers()
#members = load_memberlist()

sys.stdout.write('member,1.0\n')
sys.stdout.write('uuid,email,status,department,verified,registered\n')

if os.path.isfile(reset_filename):
	os.remove(reset_filename)

reset_file = open(reset_filename, 'w')

if not os.path.isdir(export_gpg_dir):
	os.makedirs(export_gpg_dir)

oldfiles = os.listdir(export_gpg_dir) 
for oldfile in oldfiles:
    os.remove(oldfile)

for member in members:
	if len(member.memberships) > 0 and len(member.email) > 0:
		department = member.lowestsection.fullname
		if member.ppsmembership.active:
			#status = 'eligible'
			status = 'member'
		else:
			status = 'member'
		sys.stdout.write(str(member.member_id) + ",")
		sys.stdout.write(member.email + ",")
		sys.stdout.write(status + ",")
		sys.stdout.write(department + ",")
		sys.stdout.write(str(member.verified) + ",\"\"\n")
		if member.idserverstatus >= 10:
			reset_file.write(str(member.member_id) + '\n')
			member.update_idserverstatus(member.idserverstatus - 10)
		if member.openpgp_attachement_id > 0:
			member.load_openpgp_keydata()
			keyfile = open(os.path.join(export_gpg_dir, str(member.member_id) + '.asc'), 'w')
			keyfile.write(member.openpgp_keydata)
			keyfile.close()

reset_file.close()

