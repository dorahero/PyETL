import pymongo, re

with open('./car_kind.txt', 'r', encoding='utf-8') as f:
    car_kind = f.read()
brand = car_kind.split('\n')
print(brand)

mongoclient = pymongo.MongoClient("mongodb://localhost:27017/")
mongodb = mongoclient["ucar"]
crawler_coll = mongodb['ucar_crawler']
clean_coll = mongodb['clean_db']

for doc in crawler_coll.find({}, {"_id": 0, "title": 1, "text": 1, "time": 1}):
    doc['language'] = 'zh-Hant'  # 指定語言為繁體中文 In Azure

    tmp_str = doc['text'].replace('廣  告', '').replace('\n', '')
    reg_str = re.sub(r'\(([\u4E00-\u9FA5_0-9a-zA-Z])*\)', '', tmp_str)
    doc['text'] = reg_str
    brands_show = []
    for bra in brand:
        if bra in reg_str:
            brands_show.append(bra)
    doc['brand'] = brands_show
    if len(doc['brand']) > 0:
        clean_coll.insert(doc)







