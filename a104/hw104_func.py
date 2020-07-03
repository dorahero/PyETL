import requests
from bs4 import BeautifulSoup
import os
import time
import pandas as pd

if not os.path.exists('a104'):
    os.mkdir('a104')

no_dict = ['具備駕照', '具備證照', '雇用類型',
           '代徵企業', '工作性質', '可上班日',
           '工作經歷', '語文條件', '接受身份',
           '工作技能']
notation = ['	', ' ', '\r']  # 全型空白...................
initial_col = ['職稱', '公司名稱', '產業類別', '工作連結']
f_col = ['更新日期', '職稱', '產業類別',
         '公司名稱', '上班地點', '職務類別',
         '科系要求', '學歷要求', '需求人數', '工作連結']
df = pd.DataFrame(columns=initial_col)
skill_data = []  # 每筆資料的擅長工具
data = []  # 主要資料 職稱...
data_info = []  # 每筆資料的剩餘欄位
column = []  # 所有欄位
skill_col = []  # 所有技能欄位

url = 'https://www.104.com.tw/jobs/search/?'
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64)'
                  ' AppleWebKit/537.11 (KHTML, like Gecko) '
                  'Chrome/23.0.1271.64 Safari/537.11',
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
        del work_new_dict['擅長工具']
    elif '更新日期' not in work_new_dict:
        skill_data.append([])
    if '職務類別' in work_new_dict:
        work_new_dict['職務類別'] = work_new_dict['職務類別'][:-2]
    for n in no_dict:
        if n in work_new_dict:
            del work_new_dict[n]
    return work_new_dict


def get_skill_data(s_data):
    for i, sd in enumerate(s_data):
        if len(sd) > 0:
            for s in sd:
                df[s][i] = 1


def get_data_info(info_data):
    for i, d in enumerate(info_data):
        for key in d:
            df[key][i] = d[key]


def get_initial_data(t):
    title_d = []
    title_data = []
    title_d.append(t['data-job-name'])  # 工作名稱
    title_d.append(t['data-cust-name'])  # 公司名稱
    title_d.append(t['data-indcat-desc'])  # 產業類型
    title_d.append("https:" + t.select('a')[0]['href'])  # 工作連結
    for title in title_d:
        for n in notation:
            title = title.replace(n, '')
        title_data.append(title)

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

def main_res(num, keyword, page=1):
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
        if i < (num-1):
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
        #     df['{}'.format(initial_col[x])][i] = y
    for col in col_final:
        df[col] = ''

    # get data
    # print(len(skill_data))
    get_skill_data(skill_data)
    # print(data_info)
    get_data_info(data_info)
    df.replace('', 0, inplace=True)
    # 欄位排序
    # missing_values_count = df.isnull().sum()
    # print(missing_values_count)
    # print(df.iloc[0:15, 0:3])
    print(df[['職稱', '公司名稱']].head(15))
    for i, f in enumerate(f_col):
        if f not in df.columns:
            del f_col[i]
    final_col = f_col + skill_col
    df_final = df[final_col]
    print(skill_data)
    df_final.to_csv('./a104/a104_Data_info.csv', encoding='utf8', index=False)

def main():
    n = 2
    k = 'python'
    p = 1
    main_res(n, k, p)

if __name__ == "__main__":
    main()
    # 欄位排序
    # 計算 skill 出現次數
    # 其他條件: 寫入文件
    # 職務類別是否拆項
