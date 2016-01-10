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

site_key = os.environ['CIVI_SITE_KEY']
api_key = os.environ['CIVI_API_KEY']
url = os.environ['CIVI_API_URL']
civicrm = CiviCRM(url, site_key, api_key, True)

member_id = sys.argv[1]
print("Member Id: " + member_id)
contacts = civicrm.get('Contact', external_identifier=member_id)

if len(contacts) == 1:
	contact = contacts[0]
	contact_id = contact['id']
	print("Contact Id: " + contact_id)
	print("Name: " + contact['sort_name'])
	values = civicrm.get('CustomValue', entity_id=contact_id, id=7);

	for value in values:
		print(value)
		if value['id'] == '7':
			print("Accreditation: " + value['0'])
else:
	print("Contact not found.")
