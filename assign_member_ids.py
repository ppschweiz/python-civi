#
# Pirate Party Switzerland membership management script
# Created by Stefan Thoeni at 2015-12-5
#
# Assign member ids to new members
#

from pythoncivicrm.pythoncivicrm import CiviCRM
from pythoncivicrm.pythoncivicrm import CivicrmError
from pythoncivicrm.pythoncivicrm import matches_required

def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

keyfile = open('keys', 'r')
site_key = keyfile.readline().rstrip()
api_key = keyfile.readline().rstrip()
keyfile.close()

url = 'https://members-crm.piratenpartei.ch/wp-content/plugins/civicrm/civicrm/extern/rest.php'
civicrm = CiviCRM(url, site_key, api_key, False)

#download all memberships
print('Downloading memberships...')
membership_count = civicrm.getcount('Membership')
memberships = list()

while len(memberships) < membership_count:
	memberships_download = civicrm.get('Membership', limit=400, offset=len(memberships))
	memberships.extend(memberships_download)
	print('Got ' + str(len(memberships)) + ' of ' + str(membership_count) + ' memberships');
print('Got all ' + str(len(memberships)) + ' memberships')

#download all contacts
print('Downloading contacts...')
contact_count = civicrm.getcount('Contact')
contacts = list()

while len(contacts) < contact_count:
	contacts_download = civicrm.get('Contact', limit=300, offset=len(contacts))
	contacts.extend(contacts_download)
	print('Got ' + str(len(contacts)) + ' of ' + str(contact_count) + ' contacts');
print('Got all ' + str(len(contacts)) + ' contacts')

#create list of all members (including former members)
members = dict()
for membership in memberships:
	members[membership['contact_id']] = True;

high_extid = 0

#run through all contacts and determine the current highest member id
print('Determining highest current member id...');
for contact in contacts:
	cid = contact['id']
	extid_string = contact['external_identifier']
	if is_number(extid_string):
		extid = int(extid_string)
		if high_extid < extid:
			high_extid = extid

print('Highest assigned member id is currently ' + str(high_extid))

#run through all contacts and assign new member ids where necessary
print('Assigning new member ids...');
for contact in contacts:
	cid = contact['id']
	extid_string = contact['external_identifier']
	if cid in members:
		if not(is_number(extid_string)):
			extid = high_extid + 1
			high_extid = extid
			#civicrm.update('Contact', cid, external_identifier=extid)
			print('Assiging member id ' + str(extid) + ' to contact ' + cid)

print('Highest assigned member id is currently ' + str(high_extid))

