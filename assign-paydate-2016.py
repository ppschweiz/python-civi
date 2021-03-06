# -*- coding: utf-8 -*-
#
# Pirate Party Switzerland membership management script
# Created by Stefan Thoeni at 2015-12-5
#
# Assign member ids to new members
#

import sys
import os
import datetime
import csv
import random
from pythoncivicrm.pythoncivicrm import CiviCRM
from pythoncivicrm.pythoncivicrm import CivicrmError
from pythoncivicrm.pythoncivicrm import matches_required
from piratecivi.util import is_number
from piratecivi.model import Person
from piratecivi.model import Membership
from piratecivi.factura import handle_member
from piratecivi.loader import load_all
from piratecivi.util import parse_date

site_key = os.environ['CIVI_SITE_KEY']
api_key = os.environ['CIVI_API_KEY']
url = os.environ['CIVI_API_URL']
civicrm = CiviCRM(url, site_key, api_key, True)

payed = {}
with open('paydate.csv') as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
		payed[int(row['id'])] = parse_date(row['date'], datetime.datetime(2000, 1, 1))

members = load_all(civicrm, 1, 300)

for member in members:
	if member.isppsmember:
		if member.member_id in payed:
			member.update_paymentdate(payed[member.member_id])
			lastfacdate = payed[member.member_id]  + datetime.timedelta(days=-62)
		elif member.joindate.year == 2016 and member.member_id >= 4484:
			lastfacdate = datetime.datetime(2010, 1, 1)
		elif member.joindate.year == 2016:
			lastfacdate = member.joindate + datetime.timedelta(days=-62)
		else:
			lastfacdate = datetime.datetime(2016, 1, 3) + datetime.timedelta(days=random.randint(0, 60))

		sys.stderr.write('{} : {}'.format(member.member_id, lastfacdate))

		member.update_facturadate(lastfacdate)

sys.stderr.write"done")

