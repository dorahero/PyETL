import requests
import json
import os
import re
from bs4 import BeautifulSoup

enotation = ['/', '|', '\\', '?', '\"', '*', ':', '<', '>', '.']
url = 'https://c.8891.com.tw/Models'
useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
headers = {'User-Agent': useragent}

res = requests.get(url, headers=headers)
soup = BeautifulSoup(res.text, 'html.parser')

kind_list = soup.select('div[id="brand-menu"]')[0].text.replace(' ', '').split('\n\n\n\n')
cop = re.compile("[^a-z^A-Z]")
car_list = []
for k in kind_list:
    c = cop.sub('', k.replace('\n', ''))
    if len(c) > 0:
        car_list.append(c)
print(car_list)
for car in car_list:
    with open('./8891_kind/car_log.txt', 'a', encoding='utf-8') as f:
        f.write(car + '\n')