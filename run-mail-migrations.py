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
from piratecivi.files import readfile

event = sys.argv[1]

if len(sys.argv) >= 3 and (sys.argv[2] == 'HOT'):
	dryrun = False
else:
	dryrun = True

if len(sys.argv) >= 4:
	passwords = {}
	text = readfile(sys.argv[3])
	for line in text.splitlines():
		mail = str.split(line, ',')[0]
		password = str.split(line, ',')[1]
		passwords[mail] = password
else:
	passwords = None

process_migrations(event, passwords, dryrun)

sys.stderr.write('done\n')
