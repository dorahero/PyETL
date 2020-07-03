import requests
import json
import os
from bs4 import BeautifulSoup
import time
if not os.path.exists('HOT_kind'):
    os.mkdir('HOT_kind')
ss = requests.session()

# url = 'https://www.hotcar.com.tw/UPLOAD/CW/HE3009/2213664.jpg'
url = 'https://www.hotcar.com.tw/SSAPI45/API/SPRetB?Token=VfaU%2BLJXyYZp7Nr3mFhCQtBfZ%2FrL2AQmOjkOW4W1uZVumEKn0wIHcD%2FRsdkmgB8di2Y9HFgUS%2F7HFxHm4m9eACLvfBCTdBEGoGqcd6RDUeZNSwlOrVeFarS9bEalGyz6'

s = """Connection: keep-alive
Content-Length: 188
clientID: 616905671.1591849094
Host: www.hotcar.com.tw
Origin: https://www.hotcar.com.tw
Referer: https://www.hotcar.com.tw/SSAPI45/proxyPage/proxyPage.html
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"""
cor_dict = {}
headers = {r.split(': ')[0]: r.split(': ')[1] for r in s.split('\n')}
para = {"SPNM": "CWA050Q_2018",
        "SVRNM": ["HOTCARAPP"],
        "PARMS": ["https://www.hotcar.com.tw",
                  "https://www.hotcar.com.tw/image/nophoto.png"]}
res = ss.post(url, headers=headers, json=para)
json_data = json.loads(res.text)
json_car_kind = json_data['DATA']['Table2']
car_dict = {j['MNAME1']: j['MCODE'] for j in json_car_kind}
for car in car_dict:
    print(car)
# with open('./HOT_kind/car_log.txt', 'a', encoding='utf-8') as f:
#     f.write(str(car_dict))



