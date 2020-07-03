import requests
import json
import os
from bs4 import BeautifulSoup
import re
ss = requests.session()

url = 'https://www.abccar.com.tw/abcapi/car/GetSearchCarBrand'
useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
headers = {'User-Agent': useragent}
res_1 = requests.post(url, headers=headers)
json_c = json.loads(res_1.text)
print(json_c)
BrandID = {j['BrandID']: j['Name'] for j in json_c}
print(BrandID)

# useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
# headers = {'User-Agent': useragent}
# data = {'BrandID': '75'}
# res = requests.post(url, headers=headers, json=data)
# json_c = json.loads(res.text)
# print(json_c)
# SeriesID = []
# for j in json_c:
#     SeriesID.append(j['SeriesID'])
# print(SeriesID)
count = 0
img_url = []
cid = set()
cars = 0
for f, brand in enumerate(BrandID):
    ss.cookies.clear()
    print(f, brand, BrandID[brand])
    url = 'https://www.abccar.com.tw//abcapi/search'
    useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
    data = {'brand': '{}'.format(brand),
            'tab': '1',
            'SearchType': '1',
            'BrandKey': '{}'.format(BrandID[brand][0].upper())
            }
    headers = {'User-Agent': useragent}
    res_2 = requests.post(url, headers=headers, data=data)
    json_c = json.loads(res_2.text)
    page_num = int(json_c['Total'])
    cars += page_num
    print(page_num, '輛車')
    print(int(page_num / 40) + 1, '總頁數')
    for t in range(int(page_num / 40) + 1):
        print(t+1, 'page')
        data = {'brand': '{}'.format(brand),
                'tab': '1',
                'SearchType': '1',
                'BrandKey': '{}'.format(BrandID[brand][0].upper()),
                'page': '{}'.format(t + 1),
                'series': '0',
                'category': '0',
                'SeriesGroup': '0',
                'Dealer': '0'
                }
        headers = {'User-Agent': useragent}

        res_3 = ss.post(url, headers=headers, data=data)
        try:
            json_c = json.loads(res_3.text)
            soup = BeautifulSoup(json_c['List'], 'html.parser')
            car_id = soup.select('a[class="abc-article__link"]')
            print(len(car_id), '幾輛車')
            for c in car_id:
                cid.add(str(c['car-id']) + '_' + BrandID[brand])
                count += 1
        except Exception as e:
            print(e)
print(cid)
print(len(cid))
print(cars)
cid_dict = {}
for b in BrandID:
    tmp = []
    for c in cid:
        if c[8:] == BrandID[b]:
            tmp.append(c[:7])
    cid_dict[BrandID[b]] = tmp
print(cid_dict)
with open('./abc_kind.txt', 'w', encoding='utf-8') as f:
    f.write(str(cid_dict))
# cars_num = 0
# for c in cid:
#     url = 'https://www.abccar.com.tw/car/{}?car_source=index-top-dealer'.format(c)
#     useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
#     headers = {'User-Agent': useragent}
#
#     res = requests.get(url, headers=headers)
#     soup = BeautifulSoup(res.text, 'html.parser')
#     r = re.compile(r'<[^>]*>')
#     try:
#         j = r.sub('', str(soup.select('script[type="application/ld+json"]')[0]))
#         # 轉換非法字元
#         json_car = json.loads(j)
#         img_url.append(json_car['image'])
#         cars_num += len(json_car['image'])
#     except Exception as e:
#         with open('./jsonerror.txt', 'a', encoding='utf-8') as f:
#             f.write(str(e) + str(c) + '\n')
#
# print(cars_num)


# for x in range(len(soup.select('script'))):
#     j = r.sub('', str(soup.select('script')[x]))
#     try:
#         json_car = json.loads(j)
#         if 'makesOffer' not in j:
#             continue
#         else:
#             img_url.append(json_car['makesOffer']['itemOffered']['image'])
#             count += 1
#             print(count)
#             break
#     except Exception as e:
#         print(e)
#         print("Not json")

# url = 'https://www.abccar.com.tw/abcapi/car/GetCarModelBrandSeriesCategory'
# useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
# headers = {'User-Agent': useragent}
# res = requests.get(url, headers=headers)
# json_c = json.loads(res.text)
# count = 0
# for j in json_c:
#     if 'SeriesID' in j:
#         if j['SeriesID'] in SeriesID:
#             count += 1
#             print(j)
# print(count)
# print(75, 610, 3347, 1411044)

#
# url = 'https://www.abccar.com.tw/car/1411388?car_source=index-top-dealer'
# useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
# headers = {'User-Agent': useragent}
#
# res = requests.get(url, headers=headers)
# soup = BeautifulSoup(res.text, 'html.parser')
# print(len(soup.select('script')))
# r = re.compile(r'<[^>]*>')
# j = r.sub('', str(soup.select('script')[17]))
#
# json_car = json.loads(j)
# print(json_car['makesOffer']['itemOffered']['image'])
