# -*- coding: utf-8 -*-
#
# Pirate Party Switzerland membership management script
# Created by Stefan Thoeni at 2016-11-07
#
# Error handling
#

import sys
import os
import traceback
from .sendemail import notify_admin

def handle_error(e, additional=''):
	msg = '{}\n{}\n{}\n{}'.format(type(e), e, traceback.format_exc(), additional)
	sys.stderr.write(msg + '\n')
	notify_admin('Facturer error', msg)

