from config import app
from flask import request, jsonify, url_for
from flask_cors import CORS
from sql import SQL
import datetime
import json
import funcs

import os
import base64

# import process

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
    # static = 'static'
    # dirname = '20kV及以下变电所设计规范'
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
                formulation = json.loads(formulation)
                content = formulation['content']
                for item in content:
                    if funcs.is_table(item):
                        res = funcs.tran_data(item[1])
                        SQL.insert_item(formulation_id, 'table', json.dumps(res), pics[item[2]+'.jpg'].decode('utf-8'))
                    else:
                        SQL.insert_item(formulation_id, 'text', json.dumps(item))
        else:
            return {'code': 0, 'msg': '没有数据文件'}
    else:
        return {'code': 0, 'msg': '缺少文件'}
    return {'code': 1, 'msg': '上传成功'}


@app.route('/require', methods=['POST'])
def require():
    res = request.get_json()
    if res['type'] == 1:
        data = {}
        page = res['page']
        classNum = res['classNum']
        classes = SQL.get_all_class()
        num = len(classes)
        data['totalClass'] = num
        data['pageList'] = []
        begin = classNum * page
        end = classNum * (page + 1)
        if num < begin:
            data['code'] = 0
            data['msg'] = 'fail'
            return data
        elif begin <= num < end:
            for item in classes[begin: num]:
                data['pageList'].append({'id': item[0], 'name': item[1]})
        else:
            for item in classes[begin:end]:
                data['pageList'].append({'id': item[0], 'name': item[1]})
        # print(data)
        data['code'] = 1
        data['msg'] = 'succeed'
        return data
    if res['type'] == 2:
        class_id = res['classId']
        forms = SQL.get_all_forms(class_id)
        formList = []
        for item in forms:
            formulation_id = item[0]
            result = item[2]
            content = SQL.get_items(formulation_id)
            # print(content)
            content = json.loads(content[0][2])
            content = content[0]
            if len(content) < 50:
                formList.append({'id': formulation_id, 'content': content, "result": result})
            else:
                formList.append({'id': formulation_id, 'content': content[:50], "result": result})
        return {'code': 1, 'msg': 'succeed', 'formList': formList}
    if res['type'] == 3:
        formulation_id = res['formulationId']
        itemList = []
        res = SQL.get_items(formulation_id)
        for item in res:
            print(item[2])
            itemList.append({'id': item[0], 'type': item[1], 'content': json.loads(item[2]), 'pic': item[3]})
        return {'code': 1, 'msg': '返回成功', 'itemList': itemList, "result": SQL.get_result(formulation_id)}
    return {"code": 0, "message": "请指定请求类型"}


@app.route('/save', methods=['POST'])
def save():
    data = request.get_json()['data']
    if data:
        res = {}
        keys = ['celldata', 'merge', 'title', 'shape']
        for key in keys:
            if key in data:
                res[key] = data[key]
            else:
                res[key] = None
        res = json.dumps(res)
        SQL.update_item(data['id'], res)
        return jsonify({'code': 1, 'msg': "保存成功"})
    else:
        return jsonify({'code': 0, 'msg': "保存失败"})


@app.route("/result", methods=["POST"])
def result():
    data = request.get_json()
    print(data)
    formulation_id = data.get("formulationId")
    result = data.get("result")
    if formulation_id and result:
        SQL.save_result(formulation_id, result)
        return {"code": 1, "message": "保存成功"}
    return {"code": 0, "message": "保存失败"}


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)