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
from piratecivi.bulletin import make_bulletin
from piratecivi.files import checkout_content

site_key = os.environ['CIVI_SITE_KEY']
api_key = os.environ['CIVI_API_KEY']
url = os.environ['CIVI_API_URL']
civicrm = CiviCRM(url, site_key, api_key, True)

member_id = sys.argv[1]
person = Person(civicrm, member_id=member_id)

checkout_content('bulletin');

voteid = sys.argv[2]
make_bulletin(person, voteid) 

sys.stderr.write('done\n')
