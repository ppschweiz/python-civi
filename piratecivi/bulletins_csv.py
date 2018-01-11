# -*- coding: utf-8 -*-
#
# Pirate Party Switzerland membership management script
# Created by Stefan Thoeni at 2017-06-02
#
# Create a bulletin for a member
#

import sys
import os
import csv
import datetime
import os.path

datadir = 'data/'
csvending = '.csv'

def needs_bulletin(voteid, member_id):
	filename = datadir + voteid + csvending
	if os.path.isfile(filename):
		with open(filename, newline='') as csvfile:
			csvreader = csv.reader(csvfile, delimiter=',', quotechar='\"')
			for row in csvreader:
				current_member_id = int(row[0])
				if current_member_id == member_id:
					return False
	return True

def note_sent_bulletin(voteid, member_id, bulletin_type, hashvalue):
	filename = datadir + voteid + csvending
	with open(filename, 'a', newline='') as csvfile:
		csvwriter = csv.writer(csvfile, delimiter=',', quotechar='\"', quoting=csv.QUOTE_MINIMAL)
		csvwriter.writerow([str(member_id), bulletin_type,  datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), hashvalue])

