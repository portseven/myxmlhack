import requests
import ssl
from xml.etree import ElementTree

# Define some variables we need
COMANDER_IP = '172.17.175.28'
USERNAME = 'myuser'
PASSWORD = '1234'

def getCookie():

	alldata = requests.get('https://' + COMANDER_IP + '/cgi-bin/CGILink?cmd=validate&user=' + USERNAME + '&passwd=' + PASSWORD, verify=False)
	if alldata.status_code != 200: 
		print('Screwed Up!'); 
		exit(1); 
	else: 
		events = ElementTree.fromstring(alldata.content)
		for auth in events.iter('cookie'):
			authcookie = auth.text
			return authcookie

def getReports(biscuit):

	alldata2 = requests.get('https://' + COMANDER_IP + '/cgi-bin/CGILink?cmd=vuseradmin&cookie=' + biscuit, verify=False)
	if alldata2.status_code !=200:
		print('Balls');
		exit(1);
	else:
		events2 = ElementTree.fromstring(alldata2.content)
		for reportlist in events2.iter('name'):
			print(reportlist.tag, reportlist.text)

def closeSesh(biscuit):
	alldata3 = requests.get('https://' + COMANDER_IP + '/cgi-bin/CGILink?cmd=releaseCredentail&cookie=' + biscuit, verify=False)

def main():

	biscuit = getCookie()
	getReports(biscuit)
	closeSesh(biscuit)
main() 
