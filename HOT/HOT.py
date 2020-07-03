import requests
import json
import os
from bs4 import BeautifulSoup
import time
if not os.path.exists('HOT_img'):
    os.mkdir('HOT_img')
if not os.path.exists('HOT_kind'):
    os.mkdir('HOT_kind')
if not os.path.exists('car_url'):
    os.mkdir('car_url')
ss = requests.session()
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
para_car = {"SPNM": "CWA050Q_2018",
        "SVRNM": ["HOTCARAPP"],
        "PARMS": ["https://www.hotcar.com.tw",
                  "https://www.hotcar.com.tw/image/nophoto.png"]}
res = ss.post(url, headers=headers, json=para_car)
json_data = json.loads(res.text)
json_car_kind = json_data['DATA']['Table2']
car_dict = {j['MNAME1']: j['MCODE'] for j in json_car_kind}

for i, car in enumerate(car_dict):
    if i <= 18 or car == 'TOYOTA':
        continue
    # if car == 'TOYOTA':
    #     continue
    try:
        para = {"SPNM": "CWA050Q1_2018", "SVRNM": ["HOTCARAPP"],
                "PARMS": ["https://www.hotcar.com.tw",
                          "https://www.hotcar.com.tw/image/nophoto.png",
                          "{}".format(car_dict[car]), "", 0, 0, "", "", 0, 0, "", "", "", "", "",
                          "", "", "", "", "", "", ""]}
        res = ss.post(url, headers=headers, json=para)
        json_data = json.loads(res.text)
        json_car = json_data['DATA']['Table1']
        car_img_list = []
        for j in json_car:
            car_img_list.append(j['PHOTOSTR'].split(','))
        print(car_img_list)
        if len(car_img_list) > 0:
            if not os.path.exists('./HOT_img/{}'.format(car)):
                os.mkdir('./HOT_img/{}'.format(car))
        for x, i in enumerate(car_img_list):
            for y, j in enumerate(i):
                if x == 0 and y == 0:
                    with open('./car_url/{}.txt'.format(car), 'w', encoding='utf-8') as f:
                        f.write(j + '\n')
                else:
                    with open('./car_url/{}.txt'.format(car), 'a', encoding='utf-8') as f:
                        f.write(j + '\n')

        k = 1
        for i in car_img_list:
            for j in i:
                print(k)
                try:
                    res_img = requests.get(j, headers=headers)
                    img_content = res_img.content
                    img_name = './HOT_img/{}/{}_'.format(car, car) + str(k)
                    with open(img_name + '.jpg', 'wb') as f:
                        f.write(img_content)
                        k += 1
                    with open('log.txt', 'w', encoding='utf-8') as f:
                        f.write(img_name + str(i))
                except Exception as e:
                    print(e)
                    print('此圖片被刪除')
    except Exception as e:
        print(e)

