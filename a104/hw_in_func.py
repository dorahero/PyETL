import requests
from bs4 import BeautifulSoup
import os
import time
import pandas as pd

if not os.path.exists('a104'):
    os.mkdir('a104')

no_dict = ['具備駕照', '具備證照', '雇用類型', '代徵企業', '工作性質']
notation = [' ', '\r']
initial_col = ['職稱', '公司名稱', '產業類別', '工作連結']
df = pd.DataFrame(columns=initial_col)
skill_data = []  # 每筆資料的擅長工具
data = []  # 主要資料 職稱...
data_info = []  # 每筆資料的剩餘欄位
column = []  # 所有欄位
skill_col = []  # 所有技能欄位

url = 'https://www.104.com.tw/jobs/search/?'
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive'}
ss = requests.session()


def ch_sym_to_dict(work):
    for n in notation:
        work = work.replace(n, '')
    work = work.split('\n\n\n')
    work_new = [w.replace('\n', '').replace('：', ':') for w in work]
    if len(work_new[-1]) == 0:
        work_new = work_new[:-1]
    if "其他條件:" in work_new:
        # other_cont = work_new[-1]
        # 其他條件: 寫入文件
        work_new = work_new[:-2]
    work_new_dict = {w.split(':')[0]: w.split(':')[1] for w in work_new}
    if '擅長工具' in work_new_dict:
        skill_cont = work_new_dict['擅長工具'].split('、')
        skill_data.append(skill_cont)
        for sk in skill_cont:
            if sk not in skill_col:
                skill_col.append(sk)
            pass
        del work_new_dict['擅長工具']
    elif '接受身份' in work_new_dict:
        skill_data.append([])
    if '職務類別' in work_new_dict:
        work_new_dict['職務類別'] = work_new_dict['職務類別'][:-2]
    for n in no_dict:
        if n in work_new_dict:
            del work_new_dict[n]
    return work_new_dict


def get_skill_data(sdata):
    for i, sd in enumerate(sdata):
        if len(sd) > 0:
            for s in sd:
                df[s][i] = 1
        pass


def get_data_info(info_data):
    for i, d in enumerate(info_data):
        for key in d:
            df[key][i] = d[key]


def get_initial_data(t):
    title_data = []
    title_data.append(t['data-job-name'])  # 工作名稱
    title_data.append(t['data-cust-name'])  # 公司名稱
    title_data.append(t['data-indcat-desc'])  # 產業類型
    title_data.append("https:" + t.select('a')[0]['href'])  # 工作連結

    return title_data


def re_url(params):
    res = ss.get(url, headers=headers, params=params)
    soup = BeautifulSoup(res.text, 'html.parser')
    work_title = soup.select('article[class="b-block--top-bord job-list-item b-clearfix js-job-item"]')
    for title in work_title:
        if title['data-cust-name'] in ["104外包網", "104家教網"]:
            continue
        data.append(get_initial_data(title))
        while 1:
            try:
                work_url_main = "https:" + title.select('a')[0]['href'].replace('www', 'm')
                res_work = ss.get(work_url_main, params=params, headers=headers)
                soup_work = BeautifulSoup(res_work.text, 'html.parser')
                work_address = soup_work.select('table[class="column2"]')[0].text
                break
            except IndexError as e:
                # print("......")
                time.sleep(3)
        work_add_dict = ch_sym_to_dict(work_address)
        for col in work_add_dict:
            if col not in column:
                column.append(col)
        work_content = soup_work.select('table[class="column2 condition"]')[0].text
        work_cont_dict = ch_sym_to_dict(work_content)
        for col in work_cont_dict:
            if col not in column:
                column.append(col)
        work_all_dict = {**work_add_dict, **work_cont_dict}
        data_info.append(work_all_dict)


def main():
    num = 20
    keyword = '系統'
    page = 1
    for i in range(num):
        s = """ro: 0
      kwop: 7
      keyword: {}
      order: 15
      asc: 0
      page: {}
      mode: s
      jobsource: 2018indexpoc""".format(keyword, str(page))

        params = {r.split(': ')[0]: r.split(': ')[1] for r in s.split('\n')}
        re_url(params)
        if i < (num - 1):
            print('=', end='')
        else:
            print('>Done!')
        page += 1
        time.sleep(3)
    col_f = list(set(column).difference(set(skill_col)))
    col_final = col_f + skill_col
    # print(len(data))
    for i, d in enumerate(data):
        df.loc[i] = d
        # for x, y in enumerate(d):
        #    df[initial_col[x]][i] = y
    for col in col_final:
        df[col] = ''

    # get data
    # print(len(skill_data))
    get_skill_data(skill_data)
    # print(data_info)
    get_data_info(data_info)

    # 欄位排序

    df.to_csv('./a104/a104_Data_info.csv', encoding='utf8', index=False)


if __name__ == "__main__":
    main()
    # 欄位排序
    # 計算 skill 出現次數
    # 其他條件: 寫入文件
    # 職務類別是否拆項
