import requests
import json
import os
from bs4 import BeautifulSoup
import time
import pandas as pd
import json

schema = ["id", "house_name", "address", "price(m)", "house_info", "region_name", "section_name", "house_content_info",
          "near_life", "jpg_path"]
df = pd.DataFrame(columns=schema)
region = {'台北市': 1, '新北市': 3, '桃園市': 6, '新竹市': 4,
          '新竹縣': 5, '基隆市': 2, '宜蘭縣': 21, '台中市': 8,
          '彰化縣': 10, '苗栗縣': 7, '雲林縣': 14, '南投縣': 11,
          '高雄市': 17, '台南市': 15, '嘉義市': 12, '屏東縣': 19,
          '嘉義縣': 13, '花蓮縣': 23, '台東縣': 22, '金門縣': 25,
          '澎湖縣': 24}
# tp_list = os.listdir('./台北市')
# print(tp_list)
# &firstRow=30
for i, r in enumerate(region):
    page = ''
    page_init = 0
    if not os.path.exists(r):
        os.makedirs(r)
    # if i < 10:
    #     continue
    city_json = []
    region_id = region[r]
    ss = requests.session()
    url = 'https://rent.591.com.tw/home/search/rsList?is_new_list=1&type=1&kind=0&searchtype=1&region={}'.format(region_id)
    while 1:
        try:
            if int(page) >= 0:
                page_for = (page_init + 1) * 30
                url = 'https://rent.591.com.tw/home/search/rsList?is_new_list=1&type=1&kind=0&searchtype=1&region={}&firstRow={}&totalRows={}'.format(region_id, page_for, record)
                print('-------------------', page_init)
                if page_init > page:
                    break
        except Exception as e:
            print('only one page')
            print('or the end')
        # print(url)
        s = '''Connection: keep-alive
Cookie: is_new_index=1; is_new_index_redirect=1; T591_TOKEN=i25jj8ovsqdps1ouj4gpondhl3; _ga=GA1.3.581102241.1596159674; tw591__privacy_agree=0; _ga=GA1.4.581102241.1596159674; _fbp=fb.2.1596159722085.570355555; __auc=3bbe77e3173a28c96852f6b6668; webp=1; PHPSESSID=42ffu482f5qnpni5lk10mrvl70; _gid=GA1.3.619074578.1599703039; _gid=GA1.4.619074578.1599703039; new_rent_list_kind_test=0; localTime=2; imgClick=9688505; urlJumpIp={}; urlJumpIpByTxt=%E5%8F%B0%E5%8C%97%E5%B8%82; user_index_role=1; c10f3143a018a0513ebe1e8d27b5391c=1; DETAIL[1][9691717]=1; user_browse_recent=a%3A5%3A%7Bi%3A0%3Ba%3A2%3A%7Bs%3A4%3A%22type%22%3Bi%3A1%3Bs%3A7%3A%22post_id%22%3Bs%3A7%3A%229691717%22%3B%7Di%3A1%3Ba%3A2%3A%7Bs%3A4%3A%22type%22%3Bi%3A1%3Bs%3A7%3A%22post_id%22%3Bs%3A7%3A%228161703%22%3B%7Di%3A2%3Ba%3A2%3A%7Bs%3A4%3A%22type%22%3Bi%3A1%3Bs%3A7%3A%22post_id%22%3Bs%3A7%3A%229735857%22%3B%7Di%3A3%3Ba%3A2%3A%7Bs%3A4%3A%22type%22%3Bi%3A1%3Bs%3A7%3A%22post_id%22%3Bs%3A7%3A%229762638%22%3B%7Di%3A4%3Ba%3A2%3A%7Bs%3A4%3A%22type%22%3Bi%3A1%3Bs%3A7%3A%22post_id%22%3Bs%3A7%3A%229350007%22%3B%7D%7D; _gat=1; _dc_gtm_UA-97423186-1=1; _gat_testUA=1; _gat_newHousing=1; _gat_newHousingAll=1; __asc=6bbe0a051748af369de93d9ef37; _gat_UA-97423186-1=1; last_search_type=1; index_keyword_search_analysis=%7B%22role%22%3A%221%22%2C%22type%22%3A1%2C%22keyword%22%3A%22%22%2C%22selectKeyword%22%3A%22%22%2C%22menu%22%3A%22%22%2C%22hasHistory%22%3A0%2C%22hasPrompt%22%3A0%2C%22history%22%3A0%7D; XSRF-TOKEN=eyJpdiI6Inc1R1VoZVliWWI1dEdUazJ6ZXVvR2c9PSIsInZhbHVlIjoicnRBVEJ2V1BNN0RWa29nMFdKbURPMlZqTWNKZ0lvXC9uV0UxemVORnNueWZSajJqanhCaFNvOEM2NEp5TkZ6N2xOSTk2akpHVE9IUUhUcU1pUENSVzd3PT0iLCJtYWMiOiI2MTZmOTdkYmQ1N2FhNzIyZmMzMDcxOWZhYTQxNTkxMjRmN2Q4YjM4ZTcwOGNkMzk0MTBhOGIzMjRhNTM4ZmY2In0%3D; 591_new_session=eyJpdiI6IkFhT09xTXR3NUFqVHFveEJcL0V0RjNnPT0iLCJ2YWx1ZSI6ImJSd0g0N0l0aXJyVVA5S0VvOGs2elRKQ3dadXU4d21wRVlHOGUybWZNWmYzOEJXb3VMckFJTGRhMTVFOFE5QUJGWUdiRExMTzlhdzluZGZ0bUhRWm9RPT0iLCJtYWMiOiJlOGNmNTNhMzc3MDQyZDI5NjZkNmNhNTYwMzYxNjI3YmEzNDdhNGIwZGE3NzRmYjAwYWNmNDBhM2JkMjYyNzZmIn0%3D
Host: rent.591.com.tw
Referer: https://rent.591.com.tw/?kind=0&region={}
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36
X-CSRF-TOKEN: huoUThpV7d4JCFNTKTnuQh6U7H9jZSAO7SH0SinH
X-Requested-With: XMLHttpRequest'''.format(region_id, region_id)
#         s = '''Connection: keep-alive
# Cookie: is_new_index=1; is_new_index_redirect=1; T591_TOKEN=i25jj8ovsqdps1ouj4gpondhl3; _ga=GA1.3.581102241.1596159674; tw591__privacy_agree=0; _ga=GA1.4.581102241.1596159674; _fbp=fb.2.1596159722085.570355555; __auc=3bbe77e3173a28c96852f6b6668; webp=1; PHPSESSID=42ffu482f5qnpni5lk10mrvl70; _gid=GA1.3.619074578.1599703039; _gid=GA1.4.619074578.1599703039; new_rent_list_kind_test=0; localTime=2; imgClick=9688505; last_search_type=1; index_keyword_search_analysis=%7B%22role%22%3A%222%22%2C%22type%22%3A1%2C%22keyword%22%3A%22%22%2C%22selectKeyword%22%3A%22%22%2C%22menu%22%3A%22%22%2C%22hasHistory%22%3A0%2C%22hasPrompt%22%3A0%2C%22history%22%3A0%7D; user_index_role=1; urlJumpIp={}; urlJumpIpByTxt=%E5%9F%BA%E9%9A%86%E5%B8%82; user_browse_recent=a%3A5%3A%7Bi%3A0%3Ba%3A2%3A%7Bs%3A4%3A%22type%22%3Bi%3A1%3Bs%3A7%3A%22post_id%22%3Bs%3A7%3A%229684598%22%3B%7Di%3A1%3Ba%3A2%3A%7Bs%3A4%3A%22type%22%3Bi%3A1%3Bs%3A7%3A%22post_id%22%3Bs%3A7%3A%229669233%22%3B%7Di%3A2%3Ba%3A2%3A%7Bs%3A4%3A%22type%22%3Bi%3A1%3Bs%3A7%3A%22post_id%22%3Bs%3A7%3A%229691641%22%3B%7Di%3A3%3Ba%3A2%3A%7Bs%3A4%3A%22type%22%3Bi%3A8%3Bs%3A7%3A%22post_id%22%3Bi%3A121199%3B%7Di%3A4%3Ba%3A2%3A%7Bs%3A4%3A%22type%22%3Bi%3A1%3Bs%3A7%3A%22post_id%22%3Bs%3A7%3A%229803072%22%3B%7D%7D; c10f3143a018a0513ebe1e8d27b5391c=1; _gat=1; _dc_gtm_UA-97423186-1=1; _gat_UA-97423186-1=1; 591_new_session=eyJpdiI6IlcwYzR0WmtmajVHTlhTYmJldGtZSHc9PSIsInZhbHVlIjoidHFTRTRvQ2QxQ1k3RHVUSWtndUhKQmUzNnpoZFlMaWNodDJNaHd1cjc2Z3NjWXNqTnNHalRoRHE3NGkzb3NRTGRQc0pXTXdcL21mSnZyYUJUREtpQ2lnPT0iLCJtYWMiOiJiZDQ3YjI1YjY1NWQxMjEwYTk2NGYxOWRmZGYwZDBkZDQ2MmZlMzdhNzc0ZmQ3OTQ0ZDdhNWU1MTM2YzNmYWY0In0%3D
# Host: rent.591.com.tw
# Referer: https://rent.591.com.tw/?kind=0&region={}
# Sec-Fetch-Dest: empty
# Sec-Fetch-Mode: cors
# Sec-Fetch-Site: same-origin
# User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36
# X-CSRF-TOKEN: FyqefWxcBBYCfhOM3RTCBxhZq4TXJ4IkoFACgdeq
# X-Requested-With: XMLHttpRequest'''.format(region_id, region_id)
        cor_dict = {}
        headers = {r.split(': ')[0]: r.split(': ')[1] for r in s.split('\n')}
        # para = {"SPNM": "CWA050Q_2018",
        #         "SVRNM": ["HOTCARAPP"],
        #         "PARMS": ["https://www.hotcar.com.tw",
        #                   "https://www.hotcar.com.tw/image/nophoto.png"]}
        # res = ss.post(url, headers=headers, json=para)
        res = ss.get(url, headers=headers)
        # print(res)
        json_data = json.loads(res.text)
        print(url)
        # print(json_data)
        # print(json_data['data']['data'][0]['region_name'])
        record = int(json_data['records'].replace(',', ''))
        page = int(json_data['records'].replace(',', '')) // 30
        print(page)
        # page =
        # # soup = BeautifulSoup(res.text, 'html.parser')
        tp_list = os.listdir('./{}'.format(r))
        print(len(tp_list))
        if len(tp_list) >= 1000 and i > 0:
            break
        elif len(tp_list) >= 5000:
            break
        for js in json_data['data']['data']:
            house_id = js['id']
            if str(house_id) in tp_list:
                continue
            if not os.path.exists(r + '/{}'.format(house_id)):
                os.makedirs(r + '/{}/jpg'.format(house_id))
            print(house_id)
            house_cont_url = 'https://rent.591.com.tw/rent-detail-{}.html'.format(js['id'])
            house_df = df
            house_dict = {"id": '', "house_name": '', "address": '', "price(m)": '',
                          "house_info": '', "region_name": '',
                          "section_name": '', "house_content_info": '',
                          "near_life": '', "jpg_path": r + '/{}/jpg'.format(house_id), 'house_url': ''}
            house_dict['id'] = house_id
            house_dict['house_name'] = js['fulladdress']
            house_dict['price(m)'] = js['price'] + js['unit']
            house_dict['region_name'] = js['region_name']
            house_dict['section_name'] = js['section_name']
            url_house = 'https://rent.591.com.tw/rent-detail-{}.html'.format(house_id)
            house_dict['house_url'] = url_house
            # url = 'https://hp2.591.com.tw/house/active/2019/12/27/157741954081913406_765x517.water3.jpg'
            s_house = """Connection: keep-alive
Cookie: is_new_index=1; is_new_index_redirect=1; T591_TOKEN=i25jj8ovsqdps1ouj4gpondhl3; _ga=GA1.3.581102241.1596159674; tw591__privacy_agree=0; _ga=GA1.4.581102241.1596159674; _fbp=fb.2.1596159722085.570355555; user_index_role=1; user_browse_recent=a%3A1%3A%7Bi%3A0%3Ba%3A2%3A%7Bs%3A4%3A%22type%22%3Bi%3A1%3Bs%3A7%3A%22post_id%22%3Bs%3A7%3A%227157274%22%3B%7D%7D; __auc=3bbe77e3173a28c96852f6b6668; webp=1; PHPSESSID=42ffu482f5qnpni5lk10mrvl70; urlJumpIp={}; urlJumpIpByTxt=%E6%A1%83%E5%9C%92%E5%B8%82; _gid=GA1.3.619074578.1599703039; index_keyword_search_analysis=%7B%22role%22%3A%221%22%2C%22type%22%3A%221%22%2C%22keyword%22%3A%22%22%2C%22selectKeyword%22%3A%22%22%2C%22menu%22%3A%22%22%2C%22hasHistory%22%3A0%2C%22hasPrompt%22%3A0%2C%22history%22%3A0%7D; c10f3143a018a0513ebe1e8d27b5391c=1; _gid=GA1.4.619074578.1599703039; XSRF-TOKEN=eyJpdiI6Im1nZVpKcWVPT2lTSW40T1k4U1RcL2l3PT0iLCJ2YWx1ZSI6ImQzTmJxYkJyRHBZQ0FuVVZFSTFPVnlqWHdBWk11SVZRZ0M4U1ErYlQ0eE1INEw5Z0hRaEJPVHE2b1dkVHJnU2JpRlZOb2NnSFk0ZUZSNVRkVDlBTkhRPT0iLCJtYWMiOiIxY2M5OTlhYWEwMDJlMTBjYmM1N2ZmNDE0MDA5MzQ5YzEwZDFjNDRiMmM5ZDNlOTMxZTQyYzc3NmNlZDI2ZDI0In0%3D; new_rent_list_kind_test=0; _gat=1; _dc_gtm_UA-97423186-1=1; 591_new_session=eyJpdiI6Iks1VzNLamNzQ0VJTjI2OXE1eHRTVlE9PSIsInZhbHVlIjoiUWVrTjhOODhUNVNkejkyakpGenZ4QjBnMklURzA0QllIaFk0c1JUM3NMSlNtcEphbndtOEhyTWxHU3pZclhqbk93Skk3a0lkMG5ESVhrckJybXdsVGc9PSIsIm1hYyI6IjFjM2JiOWJjZTNlN2RhNTFhN2Y4MjIzNTU5YjBiODhkZGIzOWE0ODliODBhNmQzYWYxMWY5YWI5YzMzZjdmMWEifQ%3D%3D
Host: rent.591.com.tw
Referer: https://rent.591.com.tw/?kind=0&region={}
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36
X-CSRF-TOKEN: DnMrA1qRBtAcsAudhvZv8r05f4WNMtKhkHPQ40p4
X-Requested-With: XMLHttpRequest""".format(region_id, region_id)
            cor_dict_house = {}
            headers_house = {r.split(': ')[0]: r.split(': ')[1] for r in s_house.split('\n')}
            # para = {"SPNM": "CWA050Q_2018",
            #         "SVRNM": ["HOTCARAPP"],
            #         "PARMS": ["https://www.hotcar.com.tw",
            #                   "https://www.hotcar.com.tw/image/nophoto.png"]}
            # res = ss.post(url, headers=headers, json=para)
            res_house = ss.get(url_house, headers=headers_house)
            soup_house = BeautifulSoup(res_house.text, 'html.parser')
            # addr
            try:
                address = soup_house.select('span[class="addr"]')[0].text
                house_dict['address'] = address
            except IndexError as e:
                print('no address')
            # house_content_info
            info_s = soup_house.select('div[class="detailInfo clearfix"]')[0].text + \
                     soup_house.select('div[class="leftBox"] ul[class="clearfix labelList labelList-1"]')[0].text
            house_dict['house_info'] = info_s
            house_dict['house_content_info'] = []
            house_content_dict = {}
            for f in soup_house.select('div[class="leftBox"] ul[class="facility clearfix"] li[class="clearfix"]'):
                if f.select('span')[0]['class'][0] == 'no':
                    house_content_dict[f.text] = 0
                else:
                    house_content_dict[f.text] = 1
            house_dict['house_content_info'].append(house_content_dict)
            # near
            try:
                near_life = soup_house.select('div[class="lifeBox"]')[0].text
                house_dict['near_life'] = near_life
            except IndexError as e:
                print('no life')

            # img
            s_img = '''Referer: https://rent.591.com.tw/rent-detail-{}.html
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'''.format(house_id)
            for s in soup_house.select('div[class="imgList"] li img'):
                cor_dict_img = {}
                headers_img = {r.split(': ')[0]: r.split(': ')[1] for r in s_img.split('\n')}
                print(s['src'].replace('125x85.crop', '765x517.water3'))
                url_img = s['src'].replace('125x85.crop', '765x517.water3')
                if 'null' in url_img:
                    continue
                img_id = url_img.split('_')[0].split('/')[-1]
                try:
                    res_img = ss.get(url_img, headers=headers_img, timeout=1)
                    img_content = res_img.content
                    img_name = r + '/{}/jpg/{}'.format(house_id, img_id)
                    with open(img_name + '.jpg', 'wb') as f:
                        f.write(img_content)
                except Exception as e:
                    print(e)
                    print('no picture')
            # print(house_dict)
            json_h_str = json.dumps(house_dict)
            try:
                json_f = json_h_str.encode("utf-8").decode("unicode-escape").replace('\n', '')
                print(json_f)
                with open(r + '/{}/{}.json'.format(house_id, house_id), 'w', encoding='utf-8') as f:
                    f.write(json_f)
            except Exception as e:
                print(e)
                print('encoding error')
            city_json.append(house_dict)
        time.sleep(3)
        page_init += 1
    print(city_json)
    print(len(city_json))
    # json_str = json.dumps(city_json)
    # with open(r + '/{}.json'.format(r), 'w', encoding='utf-8') as f:
    #     f.write(json_str)
    # break

