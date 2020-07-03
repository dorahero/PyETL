import requests
import json
import os
from bs4 import BeautifulSoup
import time

if not os.path.exists('8891_img'):
    os.mkdir('8891_img')
with open('./8891_kind/car_log.txt', 'r', encoding='utf-8') as f:
    car_kind = f.read()
car_kind_list = car_kind.split('\n')[:-1]
print(car_kind_list[0])
count = 0
for kind in car_kind_list:
    print(kind)
    keyword = kind.lower()
    page = 1
    url = 'https://c.8891.com.tw/Models/{}?page={}'.format(keyword, page)
    useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
    headers = {'User-Agent': useragent}

    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    try:
        car_soup = soup.select('ul[class="clearfix"]')[0].select('a')
        car_list = [car['href'] for car in car_soup]
        car_l = []
        for i in range(len(car_list)):
            if i % 2 == 0:
                car_l.append(car_list[i])
        # print(car_l)

        for c in car_l:
            res_car = requests.get(c, headers=headers)
            soup_c = BeautifulSoup(res_car.text, 'html.parser')
            print(c)
            k = '_'.join(c.split('/')[3:5])
            car_back_list = []
            try:
                url_outside = soup_c.select('div[class="summary-banner-scroll"]')[0].select('a[alt="外觀"]')[0]['href']
                pid = url_outside.split('=')[1]
                pic_list = ['%2C' + str(i) for i in range(int(pid) - 15, int(pid) + 15)]
                s = ""
                pic_str = s.join(pic_list)
                car_pic_url = 'https://c.8891.com.tw/photoLibrary-ajaxList.html?pid={}{}'.format(pid, pic_str)
                res_car_outside = requests.get(car_pic_url, headers=headers)
                json_car = json.loads(res_car_outside.text)
                for i in json_car['data']:
                    if i['tid'] == 202:
                        car_back_list.append(i)
                car_back_url = [c['thumbnail'] for c in car_back_list]
                # print(car_back_url)
                a = 1
                for img_url in car_back_url:
                    res_img = requests.get(img_url, headers=headers)
                    img_content = res_img.content
                    print(k)
                    img_name = './8891_img/' + k
                    with open(img_name + '_' + str(a) + '.png', 'wb') as f:
                        f.write(img_content)
                        count += 1
                        a += 1
            except Exception as e:
                print(e)
                print('此車已停售')

    except Exception as e:
        print(e)
        print('此款車皆完售')
    # time.sleep(3)
print(count)






