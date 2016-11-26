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

site_key = os.environ['CIVI_SITE_KEY']
api_key = os.environ['CIVI_API_KEY']
url = os.environ['CIVI_API_URL'] 
civicrm = CiviCRM(url, site_key, api_key, True)

with open(sys.argv[1]) as f:
    memberlist = f.read().splitlines()

#members = load_all(civicrm, 1, 50, True)

members = list();
for member_id in memberlist:
	onemember = load_persons(civicrm, external_identifier=member_id, progress=1, batch=20, returnfields=get_required_fields_person())
	for member in onemember:
		members.append(member)

print('member,1.0')
print('uuid,email,status,department,verified,registered')

for member in members:
	if len(member.memberships) > 0 and len(member.email) > 0 and str(member.member_id) in memberlist:
		mems = dict();
		for membership in member.memberships:
			mems[membership.name] = membership
		for membership in member.memberships:
			if membership.department.parent in mems:
				del mems[membership.department.parent]
		first = mems[mems.keys()[0]]
		department = first.department.fullname
		#if first.active:
		#	status = 'member'
		#else:
		#	status = 'eligible'
		status = 'member'
		sys.stdout.write(str(member.member_id) + ",")
		sys.stdout.write(member.email + ",")
		sys.stdout.write(status + ",")
		sys.stdout.write(department + ",")
		sys.stdout.write(str(member.verified) + ",\"\"\n")

