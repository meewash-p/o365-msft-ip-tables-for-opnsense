#!/usr/bin/python3
import json
import tempfile
from pathlib import Path
import urllib.request
import uuid
# helper to call the webservice and parse the response
def webApiGet(methodName, instanceName, clientRequestId):
    ws = "https://endpoints.office.com"
    requestPath = ws + '/' + methodName + '/' + instanceName + '?clientRequestId=' + clientRequestId
    request = urllib.request.Request(requestPath)
    with urllib.request.urlopen(request) as response:
        return json.loads(response.read().decode())
# path where client ID and latest version number will be stored
datapath = Path('/opt/.../o365_latest_ver.txt')
#datapath = Path('D:\\...\\o365_latest_ver.txt')
# path where ipv4 addressess will be saved
datapath_table = Path('/opt/.../o365_table.txt')
#datapath_table = Path('D:\\...\\o365_table.txt')

# fetch client ID and version if data exists; otherwise create new file
if datapath.exists():
    with open(str(datapath), 'r') as fin:
        clientRequestId = fin.readline().strip()
        latestVersion = fin.readline().strip()
else:
    clientRequestId = str(uuid.uuid4())
    latestVersion = '0000000000'
    with open(str(datapath), 'w') as fout:
        fout.write(clientRequestId + '\n' + latestVersion)
# call version method to check the latest version, and pull new data if version number is different
version = webApiGet('version', 'Worldwide', clientRequestId)
if version['latest'] > latestVersion:
    # write the new version number to the data file
    with open(str(datapath), 'w') as fout:
        fout.write(clientRequestId + '\n' + version['latest'])
    # invoke endpoints method to get the new data
    endpointSets = webApiGet('endpoints', 'Worldwide', clientRequestId)
    # filter results for Allow and Optimize endpoints, and transform these into tuples with port and category
    flatUrls = []
    for endpointSet in endpointSets:
        if endpointSet['category'] in ('Optimize', 'Allow'):
            category = endpointSet['category']
            urls = endpointSet['urls'] if 'urls' in endpointSet else []
            tcpPorts = endpointSet['tcpPorts'] if 'tcpPorts' in endpointSet else ''
            udpPorts = endpointSet['udpPorts'] if 'udpPorts' in endpointSet else ''
            flatUrls.extend([(category, url, tcpPorts, udpPorts) for url in urls])
    flatIps = []
    for endpointSet in endpointSets:
        if endpointSet['category'] in ('Optimize', 'Allow'):
            ips = endpointSet['ips'] if 'ips' in endpointSet else []
            category = endpointSet['category']
            tcpPorts = endpointSet['tcpPorts'] if 'tcpPorts' in endpointSet else ''
            udpPorts = endpointSet['udpPorts'] if 'udpPorts' in endpointSet else ''
            flatIps.extend([(category, ip, tcpPorts, udpPorts) for ip in ips])
    #print('IPv4 Firewall IP Address Ranges')
    #print('\n'.join(sorted(set([ip for (category, ip, tcpPorts, udpPorts) in flatIps]))))
    #print('URLs for Proxy Server')
    #print(','.join(sorted(set([url for (category, url, tcpPorts, udpPorts) in flatUrls]))))
    with open(str(datapath_table), 'w') as fout:
        fout.write('\n'.join(sorted(set([ip for (category, ip, tcpPorts, udpPorts) in flatIps]))))