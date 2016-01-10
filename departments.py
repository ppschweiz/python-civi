# -*- coding: utf-8 -*-
#
# Pirate Party Switzerland membership management script
# Created by Stefan Thoeni at 2015-12-5
#
# Assign member ids to new members
#

import sys
import os

def add_dep(deps, number, name, fullname, parent):
	deps[name] = type('test', (), {})()
	deps[name].number = number
	deps[name].fullname = fullname
	deps[name].parent = parent

def get_departments():
	deps = dict();
	add_dep(deps, 2, 'PPS', 'Piratenpartei Schweiz', None)
	add_dep(deps, 3, 'PPZH', 'Piratenpartei Zürich','PPS')
	add_dep(deps, 3, 'PPZH-Student', 'Piratenpartei Zürich','PPS')
	add_dep(deps, 4, 'PPBE', 'Piratenpartei Bern', 'PPS')
	add_dep(deps, 5, 'PPZS', 'Piratenpartei Zentralschweiz', 'PPS')
	add_dep(deps, 5, 'PPZS-Student', 'Piratenpartei Zentralschweiz', 'PPS')
	add_dep(deps, 6, 'PPBB', 'Piratenpartei beider Basel', 'PPS')
	add_dep(deps, 7, 'PPOS', 'Piratenpartei SGARAI', 'PPS')
	add_dep(deps, 8, 'PPVD', 'Parti Pirate Vaudois', 'PPS')
	add_dep(deps, 9, 'PPGE', 'Parti Pirate Genevois', 'PPS')
	add_dep(deps, 10, 'PPVS', 'Piratenpartei Wallis', 'PPS')
	add_dep(deps, 11, 'PPFR', 'Parti Pirate Fribourg', 'PPS')
	add_dep(deps, 12, 'PPNE', 'Parti Pirate Neuchâtelois','PPS')
	add_dep(deps, 13, 'PPAG', 'Piratenpartei Aargau', 'PPS')
	add_dep(deps, 14, 'PPTG', 'Piratenpartei Thurgau-Schaffhausen', 'PPS')
	add_dep(deps, 15, 'PPTI', 'Partito Pirata Ticinesi', 'PPS')
	add_dep(deps, 16, 'PPZURICH', 'Piratenpartei Stadt Zürich','PPZH')
	add_dep(deps, 17, 'PPWINTERTHUR', 'Piratenpartei Winterthur', 'PPZH')
	add_dep(deps, 18, 'PPBERN', 'Piratenpartei Stadt Bern', 'PPBE')
	return deps

