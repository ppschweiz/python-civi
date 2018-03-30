# -*- coding: utf-8 -*-
#
# Pirate Party Switzerland membership management script
# Created by Stefan Thoeni at 2016-11-26
#
# Computes member stats
#

import sys
import os
from pythoncivicrm.pythoncivicrm import CiviCRM
from pythoncivicrm.pythoncivicrm import CivicrmError
from pythoncivicrm.pythoncivicrm import matches_required
from .loader import load_all
from .sendemail import send_email
from .sendemail import notify_admin
from .errors import handle_error

stats_mail = os.environ['STATS_MAIL_ADDRESS'] 
site_key = os.environ['CIVI_SITE_KEY']
api_key = os.environ['CIVI_API_KEY']
url = os.environ['CIVI_API_URL'] 
civicrm = CiviCRM(url, site_key, api_key, True)

def process_stats():
	try:
		members = load_all(civicrm, 1, 200)
	
		stats = dict();
		for member in members:
			try:
				for membership in member.memberships:
					name = membership.department.fullname
					if not name in stats:
        					stats[name] = type('Department', (), {})()
        					stats[name].name = name
        					stats[name].members = 0
        					stats[name].voting = 0
        					stats[name].verified = 0

					stats[name].members += 1

					if membership.active:
						stats[name].voting += 1

					if member.verified:
						stats[name].verified += 1

			except Exception as e:
				handle_error(e, 'MemberId: ' + str(member.member_id))

		msg = u''
		for name in stats:
			line = u'{}: {} Mitglieder, {} Stimmberechtigte, {} Akkreditierte\n'.format(name, stats[name].members, stats[name].voting, stats[name].verified)
			msg += line
	
		send_email(u'info@piratenpartei.ch', stats_mail, u'Mitgliederstatstik', msg.replace(u'\n', u'<br/>'), msg)

	except Exception as e:
		handle_error(e)


