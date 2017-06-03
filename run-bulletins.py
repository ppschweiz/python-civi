# -*- coding: utf-8 -*-
#
# Pirate Party Switzerland membership management script
# Created by Stefan Thoeni at 2015-12-5
#
# Assign member ids to new members
#

import sys
import os
from bulletins import process_bulletins

voteid = sys.argv[1]
process_bulletins(voteid, True)

sys.stderr.write('done\n')
