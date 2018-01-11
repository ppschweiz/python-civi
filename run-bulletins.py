# -*- coding: utf-8 -*-
#
# Pirate Party Switzerland membership management script
# Created by Stefan Thoeni at 2015-12-5
#
# Assign member ids to new members
#

import sys
import os
from piratecivi.bulletins import process_bulletins

voteid = sys.argv[1]

if sys.argv[2] == 'postal':
	postal = True
elif sys.argv[2] == 'mail':
	postal = False
else:
	raise Exception()

if len(sys.argv) >= 4 and (sys.argv[3] == 'HOT'):
	dryrun = False
else:
	dryrun = True

process_bulletins(voteid, postal, dryrun)

sys.stderr.write('done\n')
