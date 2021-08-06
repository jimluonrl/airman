# airs_devices.py

import requests
from requests.auth import HTTPBasicAuth
import json
import sys



def get_request(url,request,restUser,restPassword):
    '''
    Params: bas url for ONOS REST API and a get request 
    Return: a JSON object 
    '''
    response = requests.get(url + request , auth=(restUser, restPassword))
    if response.status_code == 200 or response.status_code ==204:
        return response.json() 
    else:
        print ('{} : {}'.format (response.json()['code'], response.json()['message']))
        return -1

def post_request(url, data,restUser,restPassword):
    '''
    Params: base url for ONOS REST API and post request
    Return: HTTP status code
    '''
    response = requests.post(url, data=data, headers={"Content-Type": "application/json"}, auth=(restUser, restPassword))
    return response

def delete_request(url,request,restUser,restPassword):
    '''
    Params: base url for ONOS REST API and a delete request
    Return: HTTP status code
    '''
    response = requests.delete(url + request , auth=(restUser, restPassword))
    return response
    
def get_devices(base_url,restUser,restPassword):
    '''
    ONOS REST API: GET /devices
    Param: base url for the end point
    Return: a list of all discovered infrastructure devices 
    '''
    result = []
    devices = get_request(base_url, 'devices',restUser,restPassword)
    if devices == -1:
        return
    if len(devices) == 0:
       print('devices not found!\n')
       return result 
    for device in devices['devices']:
        record = {
        'id': device['id'],
        'type': device['type'], 
        'role': device['role'],
        'annotations': device['annotations']
        }
        result.append(record)
    result.sort(key=lambda record: record['id'])
    return result 

def get_deviceIds(base_url,restUser,restPassword):
    '''
    Param: base url for the end point 
    Return: a list of device id
    '''
    result = []
    devices = get_devices(base_url,restUser,restPassword)
    if len(devices) <= 0:
        return result 
    return [device['id'] for device in devices]   

def get_allDevicePorts(base_url,restUser,restPassword):
    '''
    ONOS REST API: GET /devices/{id}/ports
    Params: base url for the end point
    Return: a list of devices and their available ports
    '''
    result = []
    dIds = get_deviceIds(base_url,restUser,restPassword)
    if len(dIds) <= 0:  
        return result 
    for i in range(len(dIds)):
        dId = dIds[i]
        request = "devices/" + dId + "/ports"
        device = get_request(base_url, request,restUser,restPassword)
        portnums = [port['port'] for port in device['ports']] 
        record = {
        'id': device['id'],
        'ports': portnums 
        }
        result.append(record)
    return result 

def get_devicePorts(base_url, dId,restUser,restPassword):
    '''
    Params: a list of infrastructure device and a device id 
    Return a list of ports specified by the input device id
    '''
    result = []
    pList = get_allDevicePorts(base_url,restUser,restPassword)
    if len(pList) <= 0:
        return result
    for i in range(len(pList)):
        record = pList[i]
        if record['id'] == dId:
            return record['ports'] 
    return result  

def get_deviceTblSize(base_url,restUser,restPassword):
    '''
    Params: base url for ONOS REST API
    Return: table size
    '''
    return (len(get_devices(base_url,restUser,restPassword))) 

def set_port(base_url, dId, status, pId,restUser,restPassword):
    '''
    ONOS REST API: POST /devices/{id}/portstate/{port_id}
    Param: device id, port status {true,false}, device's port 
    Return HTTP status code 
    '''
    pId = str(pId) 
    if status == "true":
        data = '''{
            "enabled":true
            }'''
    else:
        data = '''{
            "enabled":false
            }'''
    url = base_url + "devices/" + dId + "/portstate/" + pId  
    response = post_request(url, data,restUser,restPassword)

def configDevicePorts(status, dId,restUser,restPassword):
    '''
    Params: status to enable or disable all poarts on specified device ID
    '''
    ports = get_devicePorts(base_url,dId,restUser,restPassword) 
    if len(ports) <= 0:
        return 
    for i in range(len(ports)):
        if ports[i] != 'local':
            set_port(base_url, dId, status, i,restUser,restPassword)


def delete_device(base_url, dId,restUser,restPassword):
    '''
    ONOs REST API: DELETE /devices/{id}
    Params: base url for the end point and a device id 
    Return HTTP status code
    '''
    '''
    #configDevicePorts('false', dId) # if ports not disabled,hosts return after ping
    # if ports disbled before deleting, device detached and hosts can't return
    # if device were to be removed, critical hosts must migrate and ports disabled
    ''' 
    request = "devices/" + dId
    delete_request(base_url, request,restUser,restPassword)

def clear_devices(base_url,restUser,restPassword):
    '''
    Params: base url to ONOS REST API
    Return: success or false
    '''
    dIds = get_deviceIds(base_url,restUser,restPassword)
    if len(dIds) <= 0:
        return
    for i in range(len(dIds)):
        print(dIds[i])
        delete_device(base_url, dIds[i],restUser,restPassword)
     
if __name__ == '__main__':

    base_url= 'http://172.17.0.5:8181/onos/v1/'

# Test fucntion call 

    deviceList = get_devices(base_url)
    size = get_deviceTblSize(base_url)
    #clear_devices(base_url)
    #dIds = get_deviceIds(base_url)
    #pList = get_allDevicePorts(base_url)
    #ports = get_devicePorts(base_url, 'of:0000000000000001')
    #response = set_port(base_url, "of:000000000000000d", "true", 7)
    #delete_device(base_url, 'of:000000000000000d')
    #configDevicePorts('true', 'of:000000000000000e')
    
