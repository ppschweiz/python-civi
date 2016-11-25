# -*- coding: utf-8 -*-
#
# Pirate Party Switzerland membership management script
# Created by Stefan Thoeni at 2016-12-25
#
# Runs the facturing process once
#

import sys
import os
from facturer import process_facturas

process_facturas();
print("done");
