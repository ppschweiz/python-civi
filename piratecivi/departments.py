# -*- coding: utf-8 -*-
#
# Pirate Party Switzerland membership management script
# Created by Stefan Thoeni at 2015-12-5
#
# Assign member ids to new members
#

import sys
import os

def add_dep(deps, number, name, fullname, parent, amount):
	deps[name] = type('Department', (), {})()
	deps[name].number = number
	deps[name].fullname = fullname
	deps[name].parent = parent
	deps[name].amount = amount

def get_departments():
	deps = dict();
	add_dep(deps, 2, 'PPS', u'Piratenpartei Schweiz', None, 80)
	add_dep(deps, 3, 'PPZH', u'Piratenpartei Zürich','PPS', 80)
	add_dep(deps, 3, 'PPZH-Student', u'Piratenpartei Zürich','PPS', 80)
	add_dep(deps, 4, 'PPBE', u'Piratenpartei Bern', 'PPS', 60)
	add_dep(deps, 5, 'PPZS', u'Piratenpartei Zentralschweiz', 'PPS', 20)
	add_dep(deps, 5, 'PPZS-Student', u'Piratenpartei Zentralschweiz', 'PPS', 20)
	add_dep(deps, 6, 'PPBB', u'Piratenpartei beider Basel', 'PPS', 20)
	add_dep(deps, 7, 'PPOS', u'Piratenpartei SGARAI', 'PPS', 25)
	add_dep(deps, 8, 'PPVD', u'Parti Pirate Vaudois', 'PPS', 20)
	add_dep(deps, 9, 'PPGE', u'Parti Pirate Genevois', 'PPS', 60)
	add_dep(deps, 10, 'PPVS', u'Piratenpartei Wallis', 'PPS', 30)
	add_dep(deps, 11, 'PPFR', u'Parti Pirate Fribourg', 'PPS', 30)
	add_dep(deps, 12, 'PPNE', u'Parti Pirate Neuchâtelois','PPS', 30)
	add_dep(deps, 13, 'PPAG', u'Piratenpartei Aargau', 'PPS', 0)
	add_dep(deps, 14, 'PPTG', u'Piratenpartei Thurgau-Schaffhausen', 'PPS', 0)
	add_dep(deps, 15, 'PPTI', u'Partito Pirata Ticinesi', 'PPS', 20)
	add_dep(deps, 16, 'PPZURICH', u'Piratenpartei Stadt Zürich','PPZH', 0)
	add_dep(deps, 17, 'PPWINTERTHUR', u'Piratenpartei Winterthur', 'PPZH', 0)
	add_dep(deps, 18, 'PPBERN', u'Piratenpartei Stadt Bern', 'PPBE', 0)
	return deps

