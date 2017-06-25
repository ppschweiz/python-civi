# -*- coding: utf-8 -*-
#
# Pirate Party Switzerland membership management script
# Created by Stefan Thoeni at 2016-12-25
#
# Runs the facturing process once
#

import sys
import os
from piratecivi.facturer import process_facturas

if len(sys.argv) >= 2 and (sys.argv[1] == 'HOT'):
	process_facturas(False)
else:
	process_facturas(True)

sys.stderr.write('done\n')

