#!/usr/bin/env python

# this script takes a csv file with user and project names,
# counts, and records the # of stars for each project
# I wrote this for convenience - to handle ''leftovers'' projects

from github3 import *
import requests
import re
import sys
import csv

# essentially does what star_count does
def main_func(adrs, authe, page_number, header, result):
	while(True):
		try:
			r = requests.get(adrs, auth=authe, params={'per_page':'100', 'page':page_number}, headers=header)
		except requests.exceptions.RequestException as e:
			print(e)
			sys.exit(1)
		matches = re.findall('20..-..-..', r.text)
	
		if not matches:
			break
		
		for i in matches:			
			if(i > '2014-01-02'):
				return
		
			result[i] = result.get(i, 0) + 1	
	
		page_number+=1

# supply your user name and password
_authe = ('user', 'password')                                                      
_header = {'Accept': 'application/vnd.github.v3.star+json'}



f = open('out2.csv')
reader = csv.reader(f)
for row in reader:
	_page_number = 1
	_result = dict()
	main_func('https://api.github.com/repos/'+row[0]+'/'+row[1]+'/stargazers', _authe, _page_number, _header, _result)
	prior_to_2014_count = 0                           
	writer = csv.writer(open('leftover.csv', 'a'), delimiter=',')	
	for k, v in sorted(_result.items()):	
		if '2014-01-02' >= k:
			prior_to_2014_count+=v		
	writer.writerow([row[0], row[1], str(prior_to_2014_count)])


