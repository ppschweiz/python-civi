# -*- coding: utf-8 -*-
#
# Pirate Party Switzerland membership management script
# Created by Stefan Thoeni at 2015-12-5
#
# Failsave update of member record

import sys
import os
import datetime
from pythoncivicrm.pythoncivicrm import CiviCRM
from pythoncivicrm.pythoncivicrm import CivicrmError
from pythoncivicrm.pythoncivicrm import matches_required

def update_entity(civicrm, entity_type, entity_id, **kwargs):
	for retry in range(1, 9):
		try:
			civicrm.update(entity_type, entity_id, **kwargs)
			return
		except CivicrmError as e:
			sys.stderr.write(str(e));
			sys.stderr.write('CiviCRM Error on update, retry {}\n'.format(retry));
	raise IOError('CiviCRM update failed permanently')

