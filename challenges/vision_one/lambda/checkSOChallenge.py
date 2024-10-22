#XDR Challenge 1, TechDay Summer 2022
import requests
import json
import os

url_path = '/v2.0/xdr/threatintel/suspiciousObjects'
# Contains a list of Vision One supported regions for ctf.
v1SupportedRegions = ["United States", "Europe", "Singapore", "Japan", "Australia", "India"]
region = {'Australia': 'https://api.au.xdr.trendmicro.com', 'Europe': 'https://api.eu.xdr.trendmicro.com',
          'India': 'https://api.in.xdr.trendmicro.com', 'Japan': 'https://api.xdr.trendmicro.co.jp',
          'Singapore': 'https://api.sg.xdr.trendmicro.com', 'United States': 'https://api.xdr.trendmicro.com'}


def checkSO(type):
    query_params = {'skipToken': "",
                        'limit': 200,
                        'type': type
                    }

    headers = {'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json;charset=utf-8'}

    r = requests.get(url_base + url_path, params=query_params, headers=headers)

    #print(r.status_code)
    if 'application/octet-stream' in r.headers.get('Content-Type', ''):
        print(json.dumps(r.json(), indent=4))
    else:
        lst = json.loads(r.text)
        lst2 = lst["data"]["suspiciousObjectList"]
        #print(json.dumps(lst2, indent=4))
        return lst2

def checkList(test_list, val_list, key):
    # Check List elements from Dictionary List
    # Using loop
    res = [any(clr == sub[key] for sub in test_list) for clr in val_list]

    # result
    print(res.count(True))
    return res.count(True)

# Main
def handler(event, context):

    key = 'value'
    v1TrendRegion = str(os.environ.get("v1TrendRegion"))
    v1AuthToken =s tr(os.environ.get("v1AuthToken"))
    url_base = region[v1TrendRegion]


    res = checkSO('domain')
    # initializing Values list
    domain_list = ['tunnel.us.ngrok.com', 'tunnel.eu.ngrok.com', 'tunnel.ap.ngrok.com', 'tunnel.au.ngrok.com',
                'tunnel.sa.ngrok.com', 'tunnel.jp.ngrok.com', 'tunnel.in.ngrok.com', 'ngrok.com', 'ngrok.io']
    ip_list = ['3.20.27.198', '3.16.250.205', '3.12.62.205', '3.134.73.173', '3.133.228.214', '3.136.132.147',
               '3.123.83.158', '3.125.234.140', '52.28.187.147', '3.122.29.226', '13.228.59.63', '18.141.102.200',
               '13.251.162.108', '52.220.69.60', '52.220.126.110', '54.153.228.243', '13.239.180.227', '13.54.73.251',
               '3.105.185.27', '3.104.168.138', '18.229.114.140', '18.229.94.125', '54.233.161.49', '18.229.186.234',
               '18.228.107.150', '52.196.202.158', '54.178.247.185', '18.177.129.29', '13.112.247.114', '18.177.245.43',
               '13.126.63.42', '13.232.212.61', '13.232.27.141', '3.6.96.240', '13.233.205.122']


    domain_success = False
    ip_success = False
    # we want 7 out of 9 to get the points
    if checkList(res, domain_list, key)>= 7:
        print("Success")
        domain_success = True
    else:
        print("Fail! on domain, need 7 out of 9")

    # we want at least 30 of the 35 to get the points
    res = checkSO('ip')
    if checkList(res, ip_list, key)>= 30:
        print("Success")
        ip_success = True
    else:
        print("Fail! on ip, need 30 out of 35")

    ctf = domain_success and ip_success
    print('success: ' + str(ctf))
    return ctf