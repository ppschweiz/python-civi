# -*- coding: utf-8 -*-
#
# Pirate Party Switzerland membership management script
# Created by Stefan Thoeni at 2015-12-5
#
# Assign member ids to new members
#

import sys
import os
import datetime
from pythoncivicrm.pythoncivicrm import CiviCRM
from pythoncivicrm.pythoncivicrm import CivicrmError
from pythoncivicrm.pythoncivicrm import matches_required
from piratecivi.util import is_number
from piratecivi.model import Person
from piratecivi.model import Membership
from piratecivi.bulletin import send_bulletin
from piratecivi.files import checkout_content

site_key = os.environ['CIVI_SITE_KEY']
api_key = os.environ['CIVI_API_KEY']
url = os.environ['CIVI_API_URL']
civicrm = CiviCRM(url, site_key, api_key, True)

member_id = sys.argv[1]
person = Person(civicrm, member_id=member_id)

checkout_content('bulletin');

voteid = sys.argv[2]

if sys.argv[3] == 'postal':
	postal = True
elif sys.argv[3] == 'mail':
	postal = False
else:
	raise Exception()

if len(sys.argv) >= 5 and (sys.argv[4] == 'HOT'):
	dryrun = False
else:
	dryrun = True

send_bulletin(person, voteid, postal, dryrun) 

sys.stderr.write('done\n')
