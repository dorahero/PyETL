import requests
import json
import os
from bs4 import BeautifulSoup
import re

url = 'https://www.abccar.com.tw/car/1416785?car_source=index-top-dealer'
useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
headers = {'User-Agent': useragent}
res = requests.get(url, headers=headers)
soup = BeautifulSoup(res.text, 'html.parser')
r = re.compile(r'<[^>]*>')
try:
    j = r.sub('', str(soup.select('script[type="application/ld+json"]')[0]))
    # 轉換非法字元
    json_car = json.loads(j)
    car_img_url = json_car['image']
    print(car_img_url)
except Exception as e:
    with open('./jsonerror.txt', 'a', encoding='utf-8') as f:
        print(e)
        f.write(str(e) + '\n')


url = 'https://www.abccar.com.tw/car/1417803?car_source=index-top-dealer'
useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
headers = {'User-Agent': useragent}
res = requests.get(url, headers=headers)
soup = BeautifulSoup(res.text, 'html.parser')
r = re.compile(r'<[^>]*>')
try:
    j = r.sub('', str(soup.select('script[type="application/ld+json"]')[0]))
    # 轉換非法字元
    json_car = json.loads(j)
    car_img_url = json_car['image']
    print(car_img_url)
except Exception as e:
    with open('./jsonerror.txt', 'a', encoding='utf-8') as f:
        print(e)
        f.write(str(e) + '\n')