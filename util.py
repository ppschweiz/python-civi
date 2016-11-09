# -*- coding: utf-8 -*-
#
# Pirate Party Switzerland membership management script
# Created by Stefan Thoeni at 2015-12-5
#
# Assign member ids to new members
#

def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

