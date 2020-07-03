from flask import Flask, request
import hw104 as hw
import json
# jsonify 回傳json

app = Flask(__name__)

@app.route('/hw104', methods=['GET', 'POST'])
def poker():
    if request.method == 'GET':
        # 將結果回傳給 /poker 以 POST 方式
        outStr = """
        <html>
            <head>
                <title>poker</title>
            </head>
            <body>
                <h1>num, keywords, page?</h1>
                <form action="/hw104" method="post">  
                    <input type="textbox" name="num">
                    <input type="textbox" name="keyword">
                    <input type="textbox" name="page">
                    <button type="submit">Submit</button>
                </form>
            </body>
        </html>
        """
        return outStr
    # elif request.method == 'POST':
    #     num = request.form.get('num')
    #     keyword = request.form.get('keyword')
    #     page = request.form.get('page')
    #     hw.main_res(int(num), keyword, int(page))
    #
    #     with open('./a104/a104_Data_info.json', encoding='utf8') as f:
    #         s = f.read()
    #
    #     json_data = json.loads(s)
    #     return json_data
        # 印 flask 一定要回傳string, 將 json 轉換為 string

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)



