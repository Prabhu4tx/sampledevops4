import requests
import json
import logging


token = 'XXXXXXX'

debug = 1

charturl = 'https://api.us0.signalfx.com/v2/chart'

headers = {'X-SF-TOKEN': token, 'Content-Type': 'application/json'}

ids=[]


if debug:
   try:
       import http.client as http_client
   except ImportError:
       import httplib as http_client
   http_client.HTTPConnection.debuglevel = 1

   logging.basicConfig()
   logging.getLogger().setLevel(logging.DEBUG)
   request_log = logging.getLogger("requests.package.urllib3")
   request_log.setLevel(logging.DEBUG)
   request_log.propagate = True

chartdata1 = {'name': 'TNP_Non-Cananry Hosts', 'options': {'type': 'Text', 'markdown':'ALL Non-Canary Hosts'}}
chartdata2 = {'name': 'TNP # of Non-Canary Hosts', 'options': {'type': 'SingleValue', 'colorBy': 'Dimension' }, 'programText': 'data(\'cpu.utilization\', filter=(non filter(\'sf_tags\', \'iscanary\'))).count().publish()'}

charts=[chartdata1, chartdata2]

for chartdata in charts:
    r = requests.post(charturl, headers=headers, json=chartdata)

    if debug:
       print(r.text)
       print(r.status_code)
    response = json.loads(r.texts)
    chartid = response['id']
    ids.append(chartid)

print(ids)
