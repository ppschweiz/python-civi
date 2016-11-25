# -*- coding: utf-8 -*-
#
# Pirate Party Switzerland membership management script
# Created by Stefan Thoeni at 2015-12-5
#
# Failsave update of member record

import sys
import os
from pythoncivicrm.pythoncivicrm import CiviCRM
from pythoncivicrm.pythoncivicrm import CivicrmError
from pythoncivicrm.pythoncivicrm import matches_required
from util import is_number
from util import parse_datetime
from util import parse_date
from util import parse_int
from departments import get_departments
import datetime

def update_entity(civicrm, entity_type, entity_id, **kwargs):
	for retry in range(1, 9):
		try:
			civicrm.update(entity_type, entity_id, **kwargs)
			return
		except CivicrmError as e:
			print('CiviCRM Error on update, retry ' + str(retry));
	raise Error('CiviCRM update failed permanently')

