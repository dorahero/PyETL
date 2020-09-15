import pandas as pd
import glob
import json
import re

col = ['id', '房屋名稱', '房屋圖片', '地址', '租金/月', '格局', '坪數', '樓層',
       '型態', '現況', '社區', '押金', '車位', '管理費', '最短租期', '開伙',
       '養寵物', '身份要求', '性別要求', '可遷入日', '法定用途', '建物面積',
       '產權登記', '桌子', '椅子', '衣櫃', '床', '沙發', '熱水器', '天然瓦斯',
       '電視', '冰箱', '冷氣', '洗衣機', '網路', '第四台', '生活機能', '附近交通',
       '圖片路徑', '房屋url']
near_col = ['生活機能', '附近交通']
info_col = ['坪數', '樓層',
            '型態', '現況', '更新於', '有效期', '社區', '押金', '車位', '管理費', '最短租期', '開伙',
            '養寵物', '身份要求', '性別要求', '隔間材料', '朝向', '可遷入日', '格局',
            '法定用途', '建物面積', '產權登記']
df = pd.DataFrame(columns=col)
r = re.compile('<[^>]*>')
print(len(col))
# pattern = info_pattern()
j_file = glob.glob('./*/*/*.json')
count = 0
for js in j_file:
    try:
        print(js)
        with open(js, 'r', encoding='utf-8') as f:
            ff = f.read().replace('\\', '').replace('.', '').replace('-', '')
            fff = r.sub('', ff)
            j = json.loads(fff)
        print(j)
        # house id
        house_dict = {'id': j['id']}
        # house name
        house_dict.update({'房屋名稱': j['house_name']})
        # house jpg
        house_dict.update({'房屋圖片': j['jpg_path']})
        # house addr
        house_dict.update({'地址': j['address']})
        # house price
        house_dict.update({'租金/月': j['price(m)']})
        # content_info
        house_dict.update(j['house_content_info'][0])
        # house_url
        house_dict.update({'房屋url': j['house_url']})
        # near life
        j_near = j['near_life'].replace(' ', '').replace('：', ' ').replace(':', ' ')
        tmp_near = []
        for near in near_col:
            a = len(j_near)
            j_near = j_near.replace(near, '')
            b = len(j_near)
            if a != b:
                tmp_near.append(near)
        near_list = [i for i in j_near.split(' ')]
        print(tmp_near)
        print(near_list[1:])
        near_dict = {tmp_near[i]: j for i, j in enumerate(near_list[1:])}
        print(near_dict)
        house_dict.update(near_dict)
        # house info
        j_info = j['house_info']
        if '車位類型' in j_info or '車位種類' in j_info or '權狀坪數' in j_info or len(j_info) - len(j_info.replace('格局', '')) > 2:
            continue
        if '格局 :' in j_info:
            j_info = '格局 :' + j_info.split('格局 :')[1]
        else:
            j_info = '坪數 :' + j_info.split('坪數 :')[1]
        j_info = j_info.replace('\xa0', '').replace('非於政府免付費公開資料可查詢', '')\
            .replace(' ', '').replace('：', ' ').replace(':', ' ')
        print(j['house_url'])
        # print(j_info)
        tmp = []
        for info in info_col:
            a = len(j_info)
            j_info = j_info.replace(info, '')
            b = len(j_info)
            if a != b:
                tmp.append(info)
        # r = pattern.match(j_info)
        info_list = [i for i in j_info.split(' ')]
        if '格局' in tmp:
            try:
                if int(info_list[1:][0][0]) > 0:
                    tmp = tmp
            except Exception as e:
                print(e)
                tmp.remove('格局')
                tmp.insert(0, '格局')
        # print(info_list[1:])
        # print(tmp)
        house_info_dict = {tmp[i]: j for i, j in enumerate(info_list[1:])}
        drop_key = []
        for key in house_info_dict:
            if key not in col:
                drop_key.append(key)
        for k in drop_key:
            house_info_dict.pop(k)
        # print(house_info_dict)
        house_dict.update(house_info_dict)
        print(house_dict)
        df = df.append(house_dict, ignore_index=True)

        count += 1
        # if len(info_list[1:]) != len(tmp):
        #     break
    except Exception as e:
        print(e)
        print(js)

print(count)
df.to_csv('./test.csv')