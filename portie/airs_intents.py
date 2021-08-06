#airs_intents.py

import requests
from requests.auth import HTTPBasicAuth
import json
import sys
import csv

from airs_config import restUser,restPassword

def get_request(url,request,restUser,restPassword):
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

def delete_request(url,request,restUser,restPassword):
    '''
    Params: basic url for RestAPI and delete request
    Return HTTP status code
    '''
    response = requests.delete(url + request , auth=(restUser, restPassword))
    return response

def post_request(url, data,restUser,restPassword):
    '''
    Params: base url for ONOS REST API and post request
    Return: HTTP status code
    '''
    response = requests.post(url, data=data, headers={"Content-Type": "application/json"}, auth=(restUser, restPassword))
    return response
 
def get_intents(base_url,restUser,restPassword):
    '''
    ONOS REST API: GET /intents
    Return: a list containing all the intents 
    '''
    
    result = []
    intents = get_request(base_url, 'intents',restUser,restPassword)
    if intents == -1:
        return
    if len(intents) == 0:
        print('intents not found!\n')
        return result 
    for intent in intents['intents']:
        record = {
        'id': intent['id'],
        'type': intent['type'],
        'key': intent['key'],
        'appId': intent['appId'],
        'state': intent['state'],
        'resources': intent['resources'] 
        } 
        result.append(record)
    return result

def get_intentKeys(base_url,restUser,restPassword):
    '''
    Params: base url for RestAPI 
    Return: a list containing installed intent's key and appId
    '''
    result = []
    intents = get_request(base_url, 'intents',restUser,restPassword)
    if intents == -1:
        return
    if len(intents) == 0:
        print('intents not found!\n')
        return result
    for intent in intents['intents']:
        record = {
        'key': intent['key'],
        'appId': intent['appId']
        }
        result.append(record)
    return result 

def get_intentFlows(base_url, appId, key,restUser,restPassword):
    '''
    ONOS REST API GET /intents/relatedflows/{appId}/{key}
    Params: base url for Rest API, intent key and appId
    Return: all flow entries of the specified intent
    '''
    request = 'intents/relatedflows/' + appId + '/' + key
    return get_request(base_url, request,restUser,restPassword) 

def post_intent(base_url, aMac, aVlan, bMac, bVlan,restUser,restPassword):
    '''
    ONOS REST API: POST /intents
    Params: base url to REST API, hostA mac, hostA vlan, hostB mac, hostB vlan
    appId needs to be verified, Random string not accepted by ONOS
    Return: HTTP status code
    '''
    aHost = aMac + "/" + aVlan
    bHost = bMac + "/" + bVlan
    record = {
    'type': 'HostToHostIntent',
    'appId': 'org.onosproject.net.intent',
    'priority': 100,
    'one': aHost,
    'two': bHost
    }
    #data = json.dumps(record, indent=2)
    #print(data) 
    url = base_url + "intents" 
    response = post_request(url, data=json.dumps(record),restUser,restPassword)
    #print(url)
    print(response)

def delete_intents(base_url, appId, key,restUser,restPassword):
    '''
    ONOs REST API: DELETE /intents/{appId}/{key}
    Params: base url to REST API, appId and key of the intent to be reomved
    Return: HTTP status code
    '''
    request = 'intents/' + appId + '/' + key
    print(request)
    return delete_request(base_url, request,restUser,restPassword)
 

if __name__ == '__main__':   

   
