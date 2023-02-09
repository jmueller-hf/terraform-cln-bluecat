import requests
import json
import argparse
import os
from time import sleep
import ipaddress


#Todo add retry logic to token endpoint
maxRetry = 3
retrySleepSeconds = 1

def raiseError(message):
    raise Exception(message)
    exit(-1)

# Generate API token for BlueCat
def generateToken(**kwargs):
    base = '{0}{1}{2}'.format('https://', kwargs['hfBamIp'], '/Services/REST/v1')
    xpath = '{0}{1}{2}{3}{4}'.format(base, '/login?username=', kwargs['username'], '&password=', kwargs['password'])
    response = requests.request("GET", xpath, verify = False)
    if response.status_code == 200:
        check = True
    else:
        check = False
    if check == True:
        returnString = response.json()
        split = returnString.split('BAMAuthToken: ')
        token = split[1].split(' <-')
        return(token[0])
    else:
        returnDict = {'Status': 'Failed', 
                    'StatusCode': response.status_code, 
                    'Reason': 'Reieved non 200 on generateToken'}
        returnJson = json.dumps(returnDict)
        return(returnJson)


def request200check(statusCode):
    if statusCode == 200:
        return(True)
    else:
        return(False)


#Format authentications headers
def headers(token):
    headers = {'Authorization': token,
                'Content-Type': 'application/json'}
    return(headers)

def postRequest(xpath, headers, body, sslVerify):
    try:
        response = requests.request("POST", xpath, headers = headers, verify = sslVerify, data=body)
        #print(response)
    except:
        response = requests.request("POST", xpath, headers = headers)
    return(response)



def createDnsRecord(hostname, ipAddress, token, **kwargs):
    base = '{0}{1}{2}'.format('https://', kwargs['hfBamIp'], '/Services/REST/v1')
    xpath = '{0}{1}'.format(base, '/addEntity?parentId=100903')
    properties = '{0}{1}{2}{3}{4}'.format('absoluteName=', hostname, 
            '.hfms.healthfirst.org|addresses=', 
            ipAddress, '|reverseRecord=true|')      
    body =  {'name': hostname,
            'type': 'HostRecord',
            'properties': properties}
    jsonBody = json.dumps(body)
    #print(jsonBody)
    header = headers(token)
    #print(headers)
    response = postRequest(xpath, header, jsonBody, False)
    #print(response.text)
    check = request200check(response.status_code)
    if check == True:
        returnDict = {'ObjectId': response.text}
        return(returnDict)
    else:
        returnDict = {'Error': response.text}
        return(returnDict)

def createCNameRecord(hostname, alias, token, **kwargs):
    base = '{0}{1}{2}'.format('https://', kwargs['hfBamIp'], '/Services/REST/v1')
    xpath = '{0}{1}'.format(base, '/addEntity?parentId=100903')
    properties = '{0}{1}{2}{3}{4}'.format('absoluteName=', hostname, 
                '.hfms.healthfirst.org|linkedRecordName=', 
                alias, "|")        
    body =  {'name': hostname,
            'type': 'AliasRecord',
            'properties': properties}
    jsonBody = json.dumps(body)
    #print(jsonBody)
    header = headers(token)
    #print(headers)
    response = postRequest(xpath, header, jsonBody, False)
    print(response.text)
    check = request200check(response.status_code)
    if check == True:
        returnDict = {'ObjectId': response.text}
        return(returnDict)
    else:
        returnDict = {'Error': response.text}
        return(returnDict)

def createExternalRecord(alias, token, **kwargs):
    base = '{0}{1}{2}'.format('https://', kwargs['hfBamIp'], '/Services/REST/v1')
    xpath = '{0}{1}'.format(base, '/addEntity?parentId=100892')
    body =  {'name': alias,
            'type': 'ExternalHostRecord',
            'properties': None}
    jsonBody = json.dumps(body)
    #print(jsonBody)
    header = headers(token)
    #print(headers)
    response = postRequest(xpath, header, jsonBody, False)
    print(response.text)
    check = request200check(response.status_code)
    if check == True:
        returnDict = {'ObjectId': response.text}
        return(returnDict)
    else:
        returnDict = {'Error': response.text}
        return(returnDict)


def is_ipv4(ipAddress):
        try:
            ipaddress.IPv4Network(ipAddress)
            return True
        except ValueError:
            return False



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=' Parameters for ')
    parser.add_argument('--hostname', dest='hostname',required=True,type=str,help='Machines hostname')
    parser.add_argument('--value', dest='value',required=True,type=str,help='IP address of host')
    parser.add_argument('--svcPassword', dest='svcPassword',required=True,type=str,help='Service Account Password')
    #parser.add_argument('--recordType', dest='recordType',required=True,type=str,help='Record Type')
    args = parser.parse_args()
    
    print(args.hostname)
    bcDict = {'username': 'svc_dns_bluecat_p', 'password': args.svcPassword, 'hfBamIp': 'bluecat.healthfirst.org'}
    token = generateToken(**bcDict)
    print(token)

    # See if Value is an IP address
    recordType = is_ipv4(args.value)

    # Creates an A record if value is an IP address
    if recordType == True:    
        print('aRecord')
        blah = createDnsRecord(args.hostname, args.value, token,**bcDict)
        print(blah)
        boops = json.dumps(blah)
        if 'ObjectId' in blah:
            print(blah)
            exit()
        else:
            print(blah)
            #exit()
      
    # Creates CName is value is not an IP address
    elif recordType == False:
        print('cname')
        if 'healthfirst.org' in args.value:
            blah = createCNameRecord(args.hostname, args.value, token, **bcDict)
            print('response', blah)
            # Creates an External Object, if host not found
            try:
                if 'Object was not found' in blah['Error']: 
                    external = createExternalRecord(args.value, token, **bcDict)
                    blah = createCNameRecord(args.hostname, args.value, token, **bcDict)
            except:
                pass
        else:
            try:
                external = createExternalRecord(args.value, token, **bcDict)
            except:
                pass
            blah = createCNameRecord(args.hostname, args.value, token, **bcDict)
        print(blah)
    if 'Error' in blah:
        exit(1)
    else:
        exit(0)



