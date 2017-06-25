# -*- coding: utf-8 -*-
#
# Pirate Party Switzerland membership management script
# Created by Stefan Thoeni at 2015-12-5
#
# Assign member ids to new members
#

import sys
import os
from piratecivi.mail_migrations import process_migrations

event = sys.argv[1]

if len(sys.argv) >= 3 and (sys.argv[2] == 'HOT'):
	dryrun = False
else:
	dryrun = True

process_migrations(event, dryrun)

sys.stderr.write('done\n')
