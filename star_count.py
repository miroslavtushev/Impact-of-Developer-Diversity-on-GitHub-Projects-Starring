# The script provides information regarding the number of stars the project had prior to 1/2/2014
# In addition, it saves the whole starring history of the project in a txt file. Just in case.

from github3 import *
from progress.bar import Bar
import requests
import re
import sys

if len(sys.argv) != 2:
	print('Wrong number of arguments!')
	print('Usage: python star_count.py owner/repo')
	sys.exit(1)

adrs = 'https://api.github.com/repos/'+str(sys.argv[1])+'/stargazers'
# supply your user name and password
authe = ('user', 'password')                            
header = {'Accept': 'application/vnd.github.v3.star+json'}

# Progress bar for convenience! *****************************************
try:
	pr_bar = requests.get(adrs, auth=authe, params={'per_page':'100'}, headers=header)
	bar_width = re.search(r'&page=(.*)', pr_bar.links['last']['url'])
	_bar_width = int(bar_width.group(1))
	bar = Bar('Making requests', fill='*', max=_bar_width)
except KeyError:
	bar = Bar('Making requests', fill='*', max=1)
# ***********************************************************************

page_number = 1
result = dict()
while(True):
    # each page will have 100 records
	r = requests.get(adrs, auth=authe, params={'per_page':'100', 'page':page_number}, headers=header)
	# searching for the date of each star
	matches = re.findall('20..-..-..', r.text)
	
    # finished collecting
	if not matches:
		break
	# count the occurrence of each date (= # of stars)
	for i in matches:
		result[i] = result.get(i, 0) + 1
	
	bar.next()
	page_number+=1
bar.finish()

prior_to_2014_count = 0                                   

# save results in a file 'user/project.txt'
filename = ''
for ch in str(sys.argv[1]):
	if ch=='/':
		ch='-'
	filename+=ch
filename+='.txt'
print(filename)

output = open(filename, 'w')	
# count how many stars occurred before the required date
for k, v in sorted(result.items()):	
	if '2014-01-02' >= k:
		prior_to_2014_count+=v
	output.write(k + ": " + str(v) + '\n')
output.write('The number of stars prior to 1/2/2014: '+str(prior_to_2014_count))
output.close()
	
print('The number of stars prior to 1/2/2014: '+str(prior_to_2014_count))
print('The data was saved in the .txt file')


