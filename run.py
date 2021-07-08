from config import app
from flask import request, jsonify, url_for
from flask_cors import CORS
from sql import SQL
import datetime
import json
import funcs

import os
import base64

import process

CORS(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    dt = datetime.datetime.now().strftime("%Y%m%d%H%M%S")  # 加个时间戳防止浏览器缓存
    # file = request.files['file']
    # filename = file.filename
    #
    # pdf_dir = 'pdf'
    # static_dir = 'static'
    #
    # file_path = os.path.join(static_dir, pdf_dir, filename)
    # file.save(file_path)
    root = 'static'
    dir = '表格图片'
    dirname = os.path.join(root, dir)
    data = process.get_all_data(dirname)
    id = 1
    for item in data:
        table_url = []
        table_image = item['table_image']
        for path in table_image:
            table_url.append(url_for('.static', _external=True, filename=dir + path.lstrip('.')+'.png') + '?' + dt)
        item['table_url'] = table_url
        item['id'] = id
        id += 1
    # pdf_url = url_for('.static', _external=True, filename='pdf/' + filename) + '?' + dt
    #
    # tables = table_extract.extract(file_path)
    return jsonify({'data': data})


@app.route('/upload', methods=['POST'])
def upload():
    static = 'static'
    dirname = '20kV及以下变电所设计规范'
    name = request.form.get('name', None)
    files = request.files.getlist('files')

    if not name:
        return {'code': 0, 'msg': '文件名为空'}
    elif SQL.is_existed(name):
        return {'code': 0, 'msg': '文件名已存在'}
    class_id = SQL.insert_class(name)
    # 暂存文件
    pics = {}
    jsn = {}
    if len(files):
        for file in files:
            filename = file.filename.split('/')
            if filename[-1] == 'data.json':
                res = file.read().decode('utf8')
                jsn[f'{filename[-1]}'] = res
            elif filename[-1].endswith('.jpg'):
                pic = file.read()
                pics[f'{filename[-1]}'] = base64.b64encode(pic)
    else:
        return {'code': 0, 'msg': '文件夹为空'}

    if jsn and pics:
        if 'data.json' in jsn:
            # 处理数据返回前端
            res = jsn['data.json'].strip()
            res = res.split("\n")
            for formulation in res:
                formulation_id = SQL.insert_formulation(class_id)
                print(formulation)
                formulation = json.loads(formulation)
                content = formulation['content']
                for item in content:
                    if funcs.is_table(item):
                        SQL.insert_item(formulation_id, 'table', json.dumps(item), pics[item[2]+'.jpg'].decode('utf8'))
                    else:
                        SQL.insert_item(formulation_id, 'text', json.dumps(item))
        else:
            return {'code': 0, 'msg': '没有数据文件'}
    else:
        return {'code': 0, 'msg': '缺少文件'}
    return {'code': 1, 'msg': '上传成功'}


# @app.route('/require', methods=['POST'])
# def require():
#

@app.route('/save', methods=['GET', 'POST'])
def save():
    root = 'static'
    dir = 'cache'
    if request.method == 'POST':
        data = request.get_data().decode("utf8")
        data = json.loads(data)['data']
        name = data[0]['class']
        cache = os.path.join(root, dir, name+'.json')
        with open(cache, 'w', encoding='utf8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        return jsonify({'success': "已保存"})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)