# airs_hosts.py

import requests
from requests.auth import HTTPBasicAuth
import json
import sys
import csv

from airs_config import restUser,restPassword

def get_request(url,request):
    '''
    Params: basic url for RestAPI and get request 
    Return a JSON object based on ONOS RestAPI
    '''

    response = requests.get(url + request , auth=(restUser, restPassword))
    if response.status_code == 200 or response.status_code == 204:
        return response.json()
    else:
        print ('{} : {}'.format (response.json()['code'], response.json()['message']))
        return -1

def delete_request(url,request):
    '''
    Params: basic url for RestAPI and delete request
    Return HTTP status code
    '''
    response = requests.delete(url + request , auth=(restUser, restPassword))
    return response
 
def get_hosts(base_url):
    '''
    ONOS REST API: GET /hosts
    Return: a list of dict containing host id, ip address, mac address
    '''
    
    result = []
    hosts = get_request(base_url, 'hosts')
    if hosts == -1:
        return
    if len(hosts) == 0:
        print('hosts not found!\n')
        return result 
    for host in hosts['hosts']:
        record = {
        'id': host['id'],
        'mac': host['mac'],
        'vlan': host['vlan'],
        'ipAddresses': host['ipAddresses'],
        'locations': host['locations'] 
        } 
        result.append(record)
    return result 

def get_hostTblSize(base_url):
    '''
    Params: base_url
    Return: host table size
    '''
    return len(get_hosts(base_url))


def clear_hosts(base_url):
    '''
    ONOS REST API: DELETE /hosts/{mac}/{vlan}
    Params: a set of hosts from get_hosts() and base_url to ONOS REST API
    and base_url
    Return: success or false
    '''
    hosts = get_hosts(base_url)
    if len(hosts) <=0:
        return
    else:
        for i in range(len(hosts)):
            host = hosts[i]
            request = "hosts/" + host['mac'] + "/" + host['vlan']
            print(request)
            response = delete_request(base_url, request)       

def get_hostInJson(hostList, ofile):
    '''
    Param: a list of dictionary containing host id, ip address mac add
    and a name of output file
    Return a Json file for all hosts
    '''
    with open(ofile, "w") as outfile:
        for host in hostList:
            host_obj = json.dumps(host, indent =4)
            outfile.write(host_obj + "\n")

def print_hosts(hostList):
    for host in hostList:
        print(host) 

if __name__ == '__main__':   

    base_url= 'http://172.17.0.5:8181/onos/v1/'

    # Test fucntion call 

    hostList = get_hosts(base_url)
    size = get_hostTblSize(base_url)
    #clear_hosts(hostList, base_url)
    #get_hostInJson(hostList, "hosts.json")

