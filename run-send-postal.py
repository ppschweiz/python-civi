# -*- coding: utf-8 -*-

import os
import sys
from piratecivi.pingen import postal_mail_file

if len(sys.argv) < 3:
	raise ValueError('Must have file and speed argument')

filename = sys.argv[1]

if sys.argv[2] == 'A':
	speed = 1
elif sys.argv[2] == 'B':
	speed = 2
else:
	raise ValueError('speed must be A or B')

if len(sys.argv) >= 4 and (sys.argv[3] == 'HOT'):
	postal_mail_file(filename, False, speed)
else:
	postal_mail_file(filename, True, speed)

sys.stderr.write('done\n')

