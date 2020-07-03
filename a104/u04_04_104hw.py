import requests
from bs4 import BeautifulSoup
import os
import time
import pandas as pd

if not os.path.exists('a104'):
    os.mkdir('a104')


df = pd.DataFrame(columns=['職稱', '公司名稱', '產業類別'])
data = []

url = 'https://www.104.com.tw/jobs/search/?'
headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
   'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
   'Accept-Encoding': 'none',
   'Accept-Language': 'en-US,en;q=0.8',
   'Connection': 'keep-alive'}
ss = requests.session()

all_dict = {}
skill_col = []
no_dict = ['具備駕照', '具備證照', '雇用類型', '代徵企業', '工作性質']
keyword = 'python'
page = 1
notation = [' ', '\r']

for i in range(3):
    s = """ro: 0
    kwop: 7
    keyword: {}
    order: 15
    asc: 0
    page: {}
    mode: s
    jobsource: 2018indexpoc""".format(keyword, str(page))

    para = {r.split(': ')[0]: r.split(': ')[1] for r in s.split('\n')}
    # print(para)
    # get 直接塞參數

    res = ss.get(url, headers=headers, params=para)
    soup = BeautifulSoup(res.text, 'html.parser')
    work_title = soup.select('article[class="b-block--top-bord job-list-item b-clearfix js-job-item"]')
    # work_url = soup.select('a[class="js-job-link"]')
    for title in work_title:
        title_data = []
        if title['data-cust-name'] in ["104外包網", "104家教網"]:
            continue
        print(title['data-job-name'])  # 工作名稱
        title_data.append(title['data-job-name'])
        print(title['data-cust-name'])  # 公司名稱
        title_data.append(title['data-cust-name'])
        print(title['data-indcat-desc'])  # 產業類型
        title_data.append(title['data-indcat-desc'])
        print("https:" + title.select('a')[0]['href'])  # 工作連結
        # 轉為手機版頁面
        while 1:
            try:
                work_url_main = "https:" + title.select('a')[0]['href'].replace('www', 'm')
                res_work = ss.get(work_url_main, params=para, headers=headers)
                soup_work = BeautifulSoup(res_work.text, 'html.parser')
                work_address = soup_work.select('table[class="column2"]')[0].text
                # work_addr = soup_work.select('a[class="addr"]')[0]['title']
                break
            except IndexError as e:
                print("......")
                time.sleep(3)
        for n in notation:
            work_address = work_address.replace(n, '')
        work_address = work_address.split('\n\n\n')
        work_addr = [w.replace('\n', '').replace('：', ':') for w in work_address]
        work_addr_dict = {w.split(':')[0]: w.split(':')[1] for w in work_addr}
        for n in no_dict:
            if n in work_addr_dict:
                del work_addr_dict[n]
        print(work_addr_dict)
        work_content = soup_work.select('table[class="column2 condition"]')[0].text
        for n in notation:
            work_content = work_content.replace(n, '')
        work_content = work_content.split('\n\n\n')
        work_cont = [w.replace('\n', '').replace('：', ':') for w in work_content]
        if len(work_cont[-1]) == 0:
            work_cont = work_cont[:-1]
        if "其他條件:" in work_cont:
            other_cont = work_cont[-1]
            # print(other_cont)
            work_cont = work_cont[:-2]
        work_cont_dict = {w.split(':')[0]: w.split(':')[1] for w in work_cont}
        if '擅長工具' in work_cont_dict:
            skill_cont = work_cont_dict['擅長工具'].split('、')
            for sk in skill_cont:
                if sk not in skill_col:
                    skill_col.append(sk)
                pass
        for n in no_dict:
            if n in work_cont_dict:
                del work_cont_dict[n]
        print(work_cont_dict)
        all_dict = work_addr_dict.copy()
        all_dict.update(work_cont_dict)

        data.append(title_data)
        print("==============================================")
        page += 1
    time.sleep(3)


columns = [col for col in all_dict]
col_final = ['職稱', '公司名稱', '產業類別'] + columns + skill_col
print(skill_col)
print(data)









