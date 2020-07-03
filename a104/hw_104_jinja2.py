from flask import Flask, request, render_template
import hw104 as hw
import pandas as pd

app = Flask(__name__, static_url_path='/static', static_folder='./static')


@app.route('/hw104', methods=['GET', 'POST'])
def hw104():
    request_method = request.method
    if request.method == 'GET':
        return render_template('s104.html')
    elif request.method == 'POST':
        keyword = request.form.get('keyword')
        num = int(request.form.get('num'))
        page = int(request.form.get('page'))
        with open('./a104/set_log.txt', 'w', encoding='utf-8') as f:
            f.write(keyword + '\n')
            f.write(str(num) + '\n')
            f.write(str(page) + '\n')
        hw1 = hw.Hw104(keyword, num, page)
        hw1.main_res()
        return render_template('w104.html',
                               request_method=request_method,
                               keyword=keyword,
                               num=num,
                               page=page)


@app.route('/hw104_w', methods=['GET', 'POST'])
def hw104_w():
    if request.method == 'GET':
        with open('./a104/a104_Data_info.csv', 'r', encoding='utf-8') as f:
            data_form = f.read().split('\n')
        data_1 = [d.split('　') for d in data_form]
        data = data_1[:-1]
        return render_template('r104.html',
                               data=data)
    if request.method == 'POST':
        with open('./a104/a104_skill_info.csv', 'r', encoding='utf-8') as f:
            skill_data_form = f.read().split('\n')[1:]
        skill_data_1 = [s.split('　') for s in skill_data_form]
        skill_data = skill_data_1[:-1]
        return render_template('rs104.html',
                               skill_data=skill_data)


@app.route('/hw104_loading', methods=['GET', 'POST'])
def hw104_loading():
    request_method = request.method
    if request.method == 'GET':
        with open('./a104/set_log.txt', 'r', encoding='utf-8') as f:
            li = f.read().split('\n')
        keyword = li[0]
        num = int(li[1])
        page = li[2]
        with open('./a104/page_log.txt', 'r', encoding='utf-8') as f:
            p = int(f.read())
        load = p*100 / num
        loading = '%.1f' % (p*100/num) + '%'
        return render_template('loading.html',
                               request_method=request_method,
                               keyword=keyword,
                               num=num,
                               page=page,
                               load=load,
                               loading=loading)


@app.route('/hw104_loc', methods=['GET', 'POST'])
def hw104_loc():
    request_method = request.method
    if request.method == 'POST':
        locate = request.form.get('locate')
        df = pd.read_csv('./a104/a104_Data_info.csv', sep='　', encoding='utf-8')
        ld = []
        for d1 in df['上班地點']:
            ld.append(d1[:2])
        df['上班縣市'] = ld
        fil = (df['上班縣市'] == locate)
        df_final = df[fil]
        df_final.to_csv('./a104/a104_Data_info_loc.csv', encoding='utf8', index=False, sep='　')
        with open('./a104/a104_Data_info_loc.csv', 'r', encoding='utf-8') as f:
            data_form = f.read().split('\n')
        data_1 = [d.split('　') for d in data_form]
        data = data_1[:-1]
        return render_template('l104.html',
                               data=data)


@app.route('/hw104_dat', methods=['GET', 'POST'])
def hw104_dat():
    request_method = request.method
    if request.method == 'POST':
        df = pd.read_csv('./a104/a104_Data_info.csv', sep='　', encoding='utf-8')
        df.sort_values('更新日期', ascending=False, inplace=True)
        df.to_csv('./a104/a104_Data_info_dat.csv', encoding='utf8', index=False, sep='　')
        with open('./a104/a104_Data_info_dat.csv', 'r', encoding='utf-8') as f:
            data_form = f.read().split('\n')
        data_1 = [d.split('　') for d in data_form]
        data = data_1[:-1]
        return render_template('d104.html',
                               data=data)


@app.route('/hw104_cop', methods=['GET', 'POST'])
def hw104_cop():
    request_method = request.method
    if request.method == 'POST':
        df = pd.read_csv('./a104/a104_Data_info.csv', sep='　', encoding='utf-8')
        df.sort_values('公司名稱', inplace=True)
        df.to_csv('./a104/a104_Data_info_cop.csv', encoding='utf8', index=False, sep='　')
        with open('./a104/a104_Data_info_cop.csv', 'r', encoding='utf-8') as f:
            data_form = f.read().split('\n')
        data_1 = [d.split('　') for d in data_form]
        data = data_1[:-1]
        return render_template('c104.html',
                               data=data)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
