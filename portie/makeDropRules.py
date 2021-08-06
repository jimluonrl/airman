# makeDropRules.py

import json
import sys
import airs_devices 

from airs_config import restUser, restPassword, nrlAppId

def buildInputFile(base_url, ethTypes, priority, timeout, ifile):
    '''
    Param: an url to the remote controller and the name of the input file
    This method obtains all the devices managed by the controller[s] and construct
    an input file that is used by buildDropFlow()
    Return: an input file in Json  
    '''
    dIds =airs_devices.get_deviceIds(base_url) 
    lst = []
    for eType in ethTypes:
        for dId in dIds:
            record = {
            'dId': dId,
            'priority': priority,
            'ethType': eType,
            'timeout': timeout
            }
            lst.append(record)
    py2Json(lst, ifile) 
    
def buildDropRecord(dId, priority, ethType, timeout):
    '''
    This method builds one drop flow at the time
    '''
    treatment = {}
    criteria = []
    record = {
    'ethType': ethType,
    'type': 'ETH_TYPE'
    }
    criteria.append(record)
    selector = {'criteria': criteria}
    record = {
    'appId' : nrlAppId,
    'priority' : priority,
    'isPermanent': 'false',
    'timeout': timeout,
    'deviceId': dId,
    'treatment': treatment,
    'selector': selector
    }
    return record

def buildDropFlows(ifile):
    '''
    Param: a Json file specifying values needed for constructing flows 
    Return: a set of flow rules for dropping packets on specifed devices  
    '''
    dropFlows = []
    data = json2Py(ifile)
    if (len(data)) <=0:
        print('invalad input file')
        return
    for i in range(len(data)):
        record = data[i]
        dId = record['dId']
        ethType = record['ethType']
        priority = record['priority']
        timeout = record['timeout']
        record = buildDropRecord(dId, priority, ethType, timeout) 
        dropFlows.append(record)
    flows = {'flows': dropFlows}
    return flows
        
def json2Py(ifile):
    with open(ifile, 'r') as f:
        return json.load(f)

def py2Json(flows, ofile):
   '''
   Param: a list of flows and the name of outfile file
   Return an output file containing flows in Json
   '''
   with open(ofile, "w") as outfile:
       jObj = json.dumps(flows, indent = 2)
       outfile.write(jObj + "\n")

if __name__ == '__main__':

    base_url= 'http://172.17.0.5:8181/onos/v1/'
    ethTypes = ['0x8cc', '0x806', '0x800']
    buildInputFile(base_url, ethTypes, 100, 60, 'in.Json') 
    py2Json(buildDropFlows('in.Json'), 'out.Json' )
