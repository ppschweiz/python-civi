# -*- coding: utf-8 -*-
#
# Pirate Party Switzerland membership management script
# Created by Stefan Thoeni at 2015-12-5
#
# Assign member ids to new members
#

import sys
import os
from departments import get_departments

def get_number(dep):
	return dep.number

deps = get_departments()

sys.stdout.write(u'department,1.0\n')
sys.stdout.write(u'id,parent,name\n')
depnums = list()

for dep in sorted(deps.values(), key=get_number):
	if not dep.number in depnums:
		sys.stdout.write(str(dep.number) + u',')
		if dep.parent == None:
			sys.stdout.write(u'None,')
		else:
			sys.stdout.write(deps[dep.parent].fullname + u',')
		sys.stdout.write(dep.fullname + u'\n')
		depnums.append(dep.number)
	
