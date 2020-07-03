import requests
import json
import os
from bs4 import BeautifulSoup
import re
import PIL.Image as Image
import time
if not os.path.exists('abc_img'):
    os.mkdir('abc_img')


with open('./abc_kind.txt', 'r', encoding='utf-8') as f:
    dict_car = eval(f.read())
# print(dict_car['VOLVO'])
count = 0
for did, d in enumerate(dict_car):
    if did != 66:
        continue
    print(did)
    print(d, ': ', len(dict_car[d]))
    count += len(dict_car[d])
    if len(dict_car[d]) == 0:
        continue
    else:
        if not os.path.exists('./abc_img/{}'.format(d)):
            os.mkdir('./abc_img/{}'.format(d))
        for i, c in enumerate(dict_car[d]):
            print(i+1, 'car in {}'.format(d))
            url = 'https://www.abccar.com.tw/car/{}?car_source=index-top-dealer'.format(c)
            useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
            headers = {'User-Agent': useragent}
            te = 0
            while 1:
                te += 1
                try:
                    res = requests.get(url, headers=headers)
                    soup = BeautifulSoup(res.text, 'html.parser')
                    r = re.compile(r'<[^>]*>')
                    try:
                        j = r.sub('', str(soup.select('script[type="application/ld+json"]')[0]))
                        # 轉換非法字元
                        json_car = json.loads(j.replace('\n', '').replace('\\', ''))
                        car_img_url = json_car['image']
                        try:
                            k = 1
                            for car_img in car_img_url:
                                test = 0
                                while 1:
                                    test += 1
                                    try:
                                        res_img = requests.get(car_img, headers=headers)
                                        img_content = res_img.content
                                        img_name = './abc_img/{}/{}_{}_'.format(d, d, (i + 1)) + str(c) + '_{}'.format(k)
                                        with open(img_name + '.jpg', 'wb') as f:
                                            f.write(img_content)

                                        im = Image.open(img_name + '.jpg')
                                        w, h = im.size
                                        im = im.convert("RGB")
                                        out = im.resize((int(w/5), int(h/5)), Image.ANTIALIAS)  # resize image with high-quality
                                        out.save(img_name + '.jpg')
                                        k += 1
                                        break
                                    except Exception as e:
                                        print(e)
                                        time.sleep(3)
                                        if test == 5:
                                            break
                        except Exception as e:
                            print(e)
                            print(car_img_url)
                            with open('./jsonerror.txt', 'a', encoding='utf-8') as f:
                                f.write(str(e) + str(c) + '\n')
                    except Exception as e:
                        print(e)
                        print(c)
                        with open('./jsonerror.txt', 'a', encoding='utf-8') as f:
                            f.write(str(e) + str(c) + '\n')
                    time.sleep(3)
                    break
                except Exception as e:
                    print(e)
                    time.sleep(3)
                    if te == 5:
                        break
    time.sleep(5)

print(count)

