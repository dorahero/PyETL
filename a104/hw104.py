import requests
from bs4 import BeautifulSoup
import os
import time
import pandas as pd

if not os.path.exists('a104'):
    os.mkdir('a104')

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


class Hw104:
    def __init__(self, keyword, num, page):
        self.keyword = keyword
        self.num = num
        self.page = page
        self.initial_col = ['職稱', '公司名稱', '產業類別', '工作連結']
        self.df = pd.DataFrame(columns=self.initial_col)
        self.skill_data = []
        self.data = []
        self.data_info = []
        self.column = []
        self.skill_col = []
        self.no_dict = ['具備駕照', '具備證照', '雇用類型',
                        '代徵企業', '工作性質', '可上班日',
                        '工作經歷', '語文條件', '接受身份']
        self.notation = ['	', ' ', '\r']
        self.f_col = ['更新日期', '職稱', '產業類別',
                      '公司名稱', '上班地點', '職務類別',
                      '科系要求', '學歷要求', '需求人數',
                      '工作連結', '擅長工具', '工作技能']
        # self.progress = tqdm(total=self.num)

    def skill_sum(self, skill):
        return self.df[skill].sum()

    def ch_sym_to_dict(self, work):
        for n in self.notation:
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
            self.skill_data.append(skill_cont)
            for sk in skill_cont:
                if sk not in self.skill_col:
                    self.skill_col.append(sk)
        elif '更新日期' not in work_new_dict:
            self.skill_data.append([])
        if '職務類別' in work_new_dict:
            work_new_dict['職務類別'] = work_new_dict['職務類別'][:-2]
        for n in self.no_dict:
            if n in work_new_dict:
                del work_new_dict[n]
        return work_new_dict

    def get_skill_data(self, s_data):
        for i, sd in enumerate(s_data):
            if len(sd) > 0:
                for s in sd:
                    self.df[s][i] = 1

    def get_data_info(self, info_data):
        for i, d in enumerate(info_data):
            for key in d:
                self.df[key][i] = d[key]

    def get_initial_data(self, t):
        title_d = []
        title_data = []
        title_d.append(t['data-job-name'])  # 工作名稱
        title_d.append(t['data-cust-name'])  # 公司名稱
        title_d.append(t['data-indcat-desc'])  # 產業類型
        title_d.append("https:" + t.select('a')[0]['href'])  # 工作連結
        for title in title_d:
            for n in self.notation:
                title = title.replace(n, '')
            title_data.append(title)
        return title_data

    def re_url(self, params):
        # self.skill_data = []  # 每筆資料的擅長工具
        # self.data = []  # 主要資料 職稱...
        # self.data_info = []  # 每筆資料的剩餘欄位
        # self.column = []  # 所有欄位
        # self.skill_col = []  # 所有技能欄位
        # self.df = pd.DataFrame(columns=initial_col)
        res = ss.get(url, headers=headers, params=params)
        soup = BeautifulSoup(res.text, 'html.parser')
        work_title = soup.select('article[class="b-block--top-bord job-list-item b-clearfix js-job-item"]')
        for title in work_title:
            if title['data-cust-name'] in ["104外包網", "104家教網"]:
                continue
            self.data.append(self.get_initial_data(title))
            while 1:
                try:
                    work_url_main = "https:" + title.select('a')[0]['href'].replace('www', 'm')
                    res_work = ss.get(work_url_main, params=params, headers=headers)
                    soup_work = BeautifulSoup(res_work.text, 'html.parser')
                    work_address = soup_work.select('table[class="column2"]')[0].text
                    break
                except IndexError as e:
                    # print(e)
                    print("......")
                    time.sleep(3)
            work_add_dict = self.ch_sym_to_dict(work_address)
            for col in work_add_dict:
                if col not in self.column:
                    self.column.append(col)
            work_content = soup_work.select('table[class="column2 condition"]')[0].text
            work_cont_dict = self.ch_sym_to_dict(work_content)
            for col in work_cont_dict:
                if col not in self.column:
                    self.column.append(col)
            work_all_dict = {**work_add_dict, **work_cont_dict}
            self.data_info.append(work_all_dict)

    def main_res(self):
        pg = self.page
        # progress = tqdm(total=self.num)
        for i in range(self.num):

            s = """ro: 0
            kwop: 7
            keyword: {}
            order: 15
            asc: 0
            page: {}
            mode: s
            jobsource: 2018indexpoc""".format(self.keyword, str(self.page))

            params = {r.split(': ')[0]: r.split(': ')[1] for r in s.split('\n')}
            pages = self.page - pg
            with open('./a104/page_log.txt', 'w', encoding='utf-8') as f:
                f.write(str(pages))
            self.re_url(params)
            if len(self.data_info) == 0:
                break
            # if i < (self.num - 1):
            #     print('=', end='')
            # else:
            #     print('>Done!')
            # self.progress.update(1)
            time.sleep(1)
            # page_now()
            self.page += 1
        col_f = list(set(self.column).difference(set(self.skill_col)))
        col_final = col_f + self.skill_col
        # print(len(data))
        for i, d in enumerate(self.data):
            self.df.loc[i] = d
            # for x, y in enumerate(d):
            #     df['{}'.format(initial_col[x])][i] = y
        for col in col_final:
            self.df[col] = ''

        # get data
        # print(len(skill_data))
        self.get_skill_data(self.skill_data)
        # print(data_info)
        self.get_data_info(self.data_info)
        self.df.replace('', 0, inplace=True)
        # 欄位排序
        # missing_values_count = df.isnull().sum()
        # print(missing_values_count)
        # print(df.iloc[0:15, 0:3])
        # print(df[['職稱', '公司名稱']].head(15))
        for i, f in enumerate(self.f_col):
            if f not in self.df.columns:
                del self.f_col[i]
        final_col = self.f_col + self.skill_col  # 排序
        df_final = self.df[final_col]
        skill_sum = {sk: self.skill_sum(sk) for sk in self.skill_col}
        df_sk = pd.DataFrame(columns=['0'])
        for s in skill_sum:
            df_sk.loc[s] = skill_sum[s]
        df_sk = df_sk.sort_values(by='0', ascending=False)
        if os.path.exists('./a104/a104_Data_info.csv'):
            with open('./a104/a104_Data_info.csv', 'w', encoding='utf-8') as f:
                f.truncate()
        if os.path.exists('./a104/a104_skill_info.csv'):
            with open('./a104/a104_skill_info.csv', 'w', encoding='utf-8') as f:
                f.truncate()
        df_final.to_csv('./a104/a104_Data_info.csv', encoding='utf8', index=False, sep='　')
        df_sk.to_csv('./a104/a104_skill_info.csv', encoding='utf8', sep='　')
        with open('./a104/page_log.txt', 'w', encoding='utf-8') as f:
            f.write(str(self.num))


def main():
    n = 1
    k = '新竹 工程師'
    p = 1
    hw = Hw104(k, n, p)
    hw.main_res()


if __name__ == "__main__":
    main()
