import requests
import json
import sys

# Define some variables we need
API_KEY = 'SOMEAPIKEY'
MERAKI_URL = 'https://dashboard.meraki.com/api/v0/'
ORG_KEY = 'SOMEORG'
headers = {'X-Cisco-Meraki-API-Key':API_KEY}

def get_net_info():

	net_list = requests.get(MERAKI_URL + 'organizations/' + ORG_KEY + '/networks', headers=headers)
	if net_list.status_code != 200: 
       		print('Incorrect Network Query String'); 
       		exit(1); 
	else: 
		json_list = json.loads(net_list.text)
		return json_list

def get_dev_info(passed_id):

	dev_list = requests.get(MERAKI_URL + 'networks/' + passed_id + '/devices', headers=headers)
	if dev_list.status_code != 200: 
       		print('Incorrect Device Query String'); 
        	exit(1); 
	else: 
		json_dlist = json.loads(dev_list.text)
		return json_dlist

def get_uplink_info(passed_serial, passed_net):

	external_ip = requests.get(MERAKI_URL + 'networks/' + passed_net + '/devices/' + passed_serial + '/uplink', headers=headers)
	if external_ip.status_code != 200:
		print('Incorrect Deivce Serial');
		exit(1);
	else:
		json_extip = json.loads(external_ip.text)
		return json_extip

def get_vlan_info(passed_net):

	vlan_data = requests.get(MERAKI_URL + 'networks/' + passed_net + '/vlans', headers=headers)
	if vlan_data.status_code != 200:
		print('Incorrect VLAN Info');
		exit(1);
	else:
		vlan_cidr = json.loads(vlan_data.text)
		return vlan_cidr

def main():

# Get list of networks and ID's
	net_data = get_net_info()
	for i in net_data:
		net_name = i["name"]
		net_id = i["id"]
# Ignore the MDM Network
		if net_name == 'MDM':
			continue
		else:
			dev_data = get_dev_info(net_id)
			for s in dev_data:
				serialno = s["serial"]
				uplink_info = get_uplink_info(serialno, net_id)
				for u in uplink_info:
					myextip = u["publicIp"]
					cidrs = get_vlan_info(net_id) 
					for c in cidrs:
						vid = c["id"]
						vnet = c["subnet"]
						print(str(net_name) + ', ' + str(myextip) + ', ' + str(vid) + ', ' + str(vnet))

main()
