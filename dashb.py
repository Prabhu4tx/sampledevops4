import requests
import json
import logging
token = 'P7bLeL2yZ14rzSg2W_5RGw'
groupid = 'FYCvzh7AgAA'

dashboardname = 'TN-P'
debug = 1

charturl = 'https://api.signalfx.com/v2/chart'
dashboardurl = 'https://api.signalfx.com/v2/dashboard'
dashboardgroupurl = 'https://api.signalfx.com/v2/dashboardgroup'

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
   requests_log = logging.getLogger("requests.packages.urllib3")
   requests_log.setLevel(logging.DEBUG)
   requests_log.propagate = True
chartdata1 = {'name': 'TNP_ Datacenter dc1', 'options' :{'type' : 'Text','markdown':'DC1 Charts'}}
chartdata2 = {'name': 'TNP_Number of hosts DC1', 'options': { 'type': 'SingleValue' }, 'programText': 'data(\'cpu.utilization\',filter=(filter(\'datacenter\', \'dc1\'))).count().publish()'}
chartdata3 = {'name': 'TNP CPU of Hosts DC1', 'options': { 'type': 'SingleValue', 'colorBy': 'Dimension' }, 'programText': 'data(\'cpu.utilization\',filter=(filter(\'datacenter\', \'dc1\'))).publish()'}
chartdata4 = {'name': 'TNP Mean CPU of Hosts DC1', 'options': { 'type': 'SingleValue', 'colorBy': 'Dimension' }, 'programText': 'data(\'cpu.utilization\',filter=(filter(\'datacenter\', \'dc1\'))).mean().publish()'}


chartdata5 = {'name': 'TNP_ Datacenter dc2', 'options' :{'type' : 'Text','markdown':'DC2 Charts'}}
chartdata6 = {'name': 'TNP_Number of hosts DC2', 'options': { 'type': 'SingleValue' }, 'programText': 'data(\'cpu.utilization\',filter=(filter(\'datacenter\', \'dc2\'))).count().publish()'}
chartdata7 = {'name': 'TNP CPU of Hosts DC2', 'options': { 'type': 'SingleValue', 'colorBy': 'Dimension' }, 'programText': 'data(\'cpu.utilization\',filter=(filter(\'datacenter\', \'dc2\'))).publish()'}
chartdata8 = {'name': 'TNP Mean CPU of Hosts DC2', 'options': { 'type': 'SingleValue', 'colorBy': 'Dimension' }, 'programText': 'data(\'cpu.utilization\',filter=(filter(\'datacenter\', \'idc2\'))).mean().publish()'}

chartdata9 = {'name': 'TNP_ Datacenter dc3', 'options' :{'type' : 'Text','markdown':'DC3 Charts'}}
chartdata10 = {'name': 'TNP_Number of hosts DC3', 'options': { 'type': 'SingleValue' }, 'programText': 'data(\'cpu.utilization\',filter=(filter(\'datacenter\', \'dc3\'))).count().publish()'}
chartdata11 = {'name': 'TNP CPU of Hosts DC3', 'options': { 'type': 'SingleValue', 'colorBy': 'Dimension' }, 'programText': 'data(\'cpu.utilization\',filter=(filter(\'datacenter\', \'dc3\'))).publish()'}
chartdata12 = {'name': 'TNP Mean CPU of Hosts DC3', 'options': { 'type': 'SingleValue', 'colorBy': 'Dimension' }, 'programText': 'data(\'cpu.utilization\',filter=(filter(\'datacenter\', \'dc3\'))).mean().publish()'}

chartdata13 = {'name': 'TNP_ Datacenter dc4', 'options' :{'type' : 'Text','markdown':'DC4 Charts'}}
chartdata14 = {'name': 'TNP_Number of hosts DC4', 'options': { 'type': 'SingleValue' }, 'programText': 'data(\'cpu.utilization\',filter=(filter(\'datacenter\', \'dc4\'))).count().publish()'}
chartdata15 = {'name': 'TNP CPU of Hosts DC4', 'options': { 'type': 'SingleValue', 'colorBy': 'Dimension' }, 'programText': 'data(\'cpu.utilization\',filter=(filter(\'datacenter\', \'dc4\'))).publish()'}
chartdata16 = {'name': 'TNP Mean CPU of Hosts DC4', 'options': { 'type': 'SingleValue', 'colorBy': 'Dimension' }, 'programText': 'data(\'cpu.utilization\',filter=(filter(\'datacenter\', \'dc4\'))).mean().publish()'}

#8. INCLUDE THE CHARTDATA LINES FOR EACH CHART ABOVE HERE. FOR EXAMPLE: charts=[chartdata1, chartdata2, chartdata3]
charts=[chartdata1, chartdata2, chartdata3, chartdata4, chartdata5,chartdata6, chartdata7, chartdata8, chartdata9, chartdata10, chartdata11, chartdata12, chartdata13, chartdata14, chartdata15, chartdata16]


for chartdata in charts:
  # Hit the Splunk IM API endpoint to push the chart
    r = requests.post(charturl, headers=headers, json=chartdata)

# If debug is turned on, print JSON response and HTTP status code
    if debug:
       print(r.text)
       print(r.status_code)

# Extract id of just-created chart from JSON response
    response = json.loads(r.text)
    chartid = response['id']
    ids.append(chartid)

print(ids)

# Create new dashboard and add above charts
col=0
row=1
height=1
width=3
chartlines=""
groupId = 1

#building the string for charts
for chid in ids:
    chartsn= '\"chartId\":\"{}\",\"column\": {} , \"height\": {}, \"row\":{}, \"width\": {} '.format(chid, col, height, row, width) 
    chartsn="{" + chartsn + "}"
    # check if need to add comma between the each chart entry
    if(len(chartlines) > 1):
        chartlines = chartlines + "," 
    
    chartlines =chartlines + chartsn
    col=col+3
    if(col>9):
        row=row+1
        col = 0
#print('chartlines', chartlines)

#building the string for dashboard data 
dashboarddata = "{\"name\":\"" + dashboardname + "\", \"groupId\":\""+ groupid +"\",\"charts\":[" + chartlines + "]}"

#Converting string to valid JSON
dashboarddata =json.loads(dashboarddata) 

#Request to post dashboard
r = requests.post(dashboardurl, headers=headers, json=dashboarddata)

# If debug is turned on, print JSON response and HTTP status code
if debug:
   print(r.text)
   print(r.status_code)


