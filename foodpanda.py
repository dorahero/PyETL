import pandas as pd
import glob
from sqlalchemy import create_engine

engine = create_engine('mysql+pymysql://root:red@mysql/foodpanda')

fff = glob.glob('./csv/store*.csv')
id_list = []

for ff in fff:
  # print(ff)
  df = pd.read_csv(ff)
  for d in df['id'].unique():
    id_list.append(str(d))

from datetime import datetime, timedelta
date = datetime.now().strftime('%Y%m%d%H%M%S')


import requests
import json
import os
from bs4 import BeautifulSoup
import time
import re
import pandas as pd
from tqdm.auto import tqdm

store_col = ['id', 'city', 'name', 'characteristics', 'address', 'rating', 'phone', 'url', 'latitude', 'longitude']
menus_col = ['id', 'categories', 'name', 'price']
schedule_col = ['id', 'week', 'open', 'close']
df_store = pd.DataFrame(columns=store_col)
df_menus = pd.DataFrame(columns=menus_col)
df_sh = pd.DataFrame(columns=schedule_col)
cop = re.compile("[^\u4e00-\u9fa5^a-z^A-Z^0-9]")
cop2 = re.compile("[^\u4e00-\u9fa5^0-9]")
# city name
url = 'https://www.foodpanda.com.tw'
s = '''user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'''
headers = {r.split(': ')[0]: r.split(': ')[1] for r in s.split('\n')}

res = requests.get(url, headers=headers)
soup = BeautifulSoup(res.text, 'html.parser')
domain = 'https://www.foodpanda.com.tw'
store_list = []
city_dict = {}
for s in soup.select('ul.city-list a'):
    city = cop.sub('', s.select('.city-name')[0].text)
    city_dict[city] = domain + s['href']
# store web
for c in tqdm(city_dict):
    url = city_dict[c]
    s = '''user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'''
    headers = {r.split(': ')[0]: r.split(': ')[1] for r in s.split('\n')}

    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    domain = 'https://www.foodpanda.com.tw'
    store_list = []
    ss = soup.select('div.restaurants__list')[0]
    for s in ss.select('a'):
        store = {}
        store['id'] = s['data-vendor-id']
        store['name'] = s.select('span[class="name fn"]')[0].text
        store['url'] = domain + s['href']
        if store['id'] not in id_list:
          store_list.append(store)
        else:
          # print(store['id'])
          continue
    # menu
    for s_id in tqdm(store_list):
        store_info = {}
        url = 'https://www.foodpanda.com.tw/api/v1/vendors/{}'.format(s_id['id'])
        s = '''accept: application/json
referer: {}
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36
x-requested-with: XMLHttpRequest'''.format(s_id['url'])
        headers = {r.split(': ')[0]: r.split(': ')[1] for r in s.split('\n')}

        res = requests.get(url, headers=headers)
        json_data = json.loads(res.text)
        try:
          store_info['id'] = s_id['id']
          store_info['city'] = c
          store_info['name'] = json_data['name']
          ch_list = []
          for characteristics in json_data['food_characteristics']:
            ch_list.append(cop.sub('', characteristics['name']))
          store_info['characteristics'] =  ' '.join(ch_list)
          store_info['address'] = cop2.sub('', json_data['address'])
          store_info['latitude'] = json_data['latitude']
          store_info['longitude'] = json_data['longitude']
          menus = json_data['menus']
          try:
            menu_categories = menus[0]['menu_categories']
          except IndexError as e:
            menu_categories = []
            with open('Error_log.txt', 'a', encoding='utf-8') as f:
              f.write(str(e) + ":" + s_id['url'] + '\n')
          for m in menu_categories:
              # print(m['name'])
              for p in m['products']:
                  product = {}
                  product['id'] = store_info['id']
                  product['categories'] = m['name']
                  product['name'] = p['name']
                  product['price'] = int(p['product_variations'][0]['price'])
                  df_menus = df_menus.append(product, ignore_index=True)
          for s in json_data['schedules']:
            if s['opening_type'] == "delivering":
              schedule_dict = {}
              schedule_dict['id'] = store_info['id']
              schedule_dict['week'] = s['weekday']
              schedule_dict['open'] = s['opening_time']
              schedule_dict['close'] = s['closing_time']
              df_sh = df_sh.append(schedule_dict, ignore_index=True)
          store_info['rating'] = json_data['rating']
          store_info['phone'] = json_data['customer_phone']
          store_info['url'] = s_id['url']
          df_store = df_store.append(store_info, ignore_index=True)
          if os.path.exists('./csv/store_{}.csv'.format(date)):
            df_store.to_csv('./csv/store_{}.csv'.format(date), mode='a', header=False)
            df_menus.to_csv('./csv/menus_{}.csv'.format(date), mode='a', header=False)
            df_sh.to_csv('./csv/schedule_{}.csv'.format(date), mode='a', header=False)
          else:
            df_store.to_csv('./csv/store_{}.csv'.format(date), mode='a')
            df_menus.to_csv('./csv/menus_{}.csv'.format(date), mode='a')
            df_sh.to_csv('./csv/schedule_{}.csv'.format(date), mode='a')
          df_store.to_sql('store', engine, index = False, if_exists='append')
          df_menus.to_sql('menu', engine, index = False, if_exists='append')
          df_sh.to_sql('schedule', engine, index = False, if_exists='append')
          df_store = df_store.iloc[0:0]
          df_sh = df_sh.iloc[0:0]
          df_menus = df_menus.iloc[0:0]
        except Exception as e:
          with open('Error_log.txt', 'a', encoding='utf-8') as f:
            f.write(str(e) + ":" + s_id['id'] + '\n')
