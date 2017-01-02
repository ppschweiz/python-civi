# -*- coding: utf-8 -*-
#
# Pirate Party Switzerland membership management script
# Created by Stefan Thoeni at 2016-12-26
#
# Runs the stats process once
#

import sys
import os
from stats import process_stats

process_stats();

sys.stderr.write('done\n')

