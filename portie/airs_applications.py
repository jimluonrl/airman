# airs_applications.py

import requests
from requests.auth import HTTPBasicAuth
import json
import sys

from airs_config import restUser,restPassword


whiteList = []
lst = ['org.onosproject.drivers', 'org.onosproject.hostprovider', 'org.onosproject.lldpprovider', 'org.onosproject.openflow-base', 'org.onosproject.openflow', 'org.onosproject.optical-model', 'org.onosproject.proxyarp', 'org.onosproject.fwd', 'org.onosproject.layout']

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
 
def get_apps(base_url):
    '''
    ONOS REST API: GET /applications
    Return: a list of installed applcations 
    '''
    
    result = []
    apps = get_request(base_url, 'applications')
    if apps == -1:
        return
    if len(apps) == 0:
        print('applications not found!\n')
        return result 
    for app in apps['applications']:
        record = {
        'name': app['name'],
        'id': app['id'],
        'version': app['version'],
        'state': app['state'],
        'origin': app['origin'],
        'category': app['category'],
        'permissions': app['permissions'],
        'requiredApps': app['requiredApps']
        } 
        result.append(record)
    return result 

def get_appIds(base_url):
    '''
    ONOS REST API: GET /applications/ids
    Return: a set of application IDs  
    '''
    request = 'applications/ids'
    return get_request(base_url, request)

def get_appByName(base_url, appName):
    '''
    ONOS REST API: GET /applications/{name}
    Param: base url and application name
    Return: details of the specified application
    '''
    request = 'applications/' + appName
    return get_request(base_url, request)

def delete_appByName(base_url, appName):
    '''
    ONOS REST API: DELETE /applications/{name}
    Param: base url and application name 
    Return: Unstalls the speficied application
    '''
    app = get_appByName(base_url, appName)
    if app == -1:
        return
    deActive_appByName(base_url, appName)
    if appName in whiteList: # this assumes core applications not compromised
        return print('Error: delete core applications not allowed')
     
    request = 'applications/' + appName
    print(request)
    return delete_request(base_url, request)

def deActive_appByName(base_url, appName):
    '''
    ONOS REST API: DELETE /applications/{name}/active
    Params: base url and application name to be de-active
    REturn: HTTP status code
    '''
    request = 'applications/' + appName + '/active'
    return delete_request(base_url, request) 

def set_whitelistApp(list):
    '''
    Param: a list of appications that need to be white-listed
    Return: a white listed application ID
    '''
    global whiteList
    if(len(list) > len(whiteList)):
        whiteList = list[:]


if __name__ == '__main__':   

    base_url= 'http://172.17.0.5:8181/onos/v1/'
    set_whitelistApp(lst)
    # Test fucntion call 

    apps = get_apps(base_url)
    ids = get_appIds(base_url)
    app = get_appByName(base_url, 'org.onosproject.ovsdb-base')
    deActive_appByName(base_url, 'org.onosproject.ovsdb-basedfdfdf')
    delete_appByName(base_url, 'org.onosproject.hostprovider') 
