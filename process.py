import os
import re
import json
from bim_table import ocr_api, save_ocr_data


def get_all_data(dirname):
    pattern = '<table>(.+)</table>'
    res = []
    for root, dirs, files in os.walk(dirname):
        jsn = files
        break
    for file in jsn:
        name = file.rstrip('.json')
        filename = os.path.join(dirname, file)
        print(filename)
        with open(filename, 'r', encoding='utf-8') as f:
            data = f.readlines()
            for item in data:
                item = json.loads(item)
                res.append(item)
    return res


def get_all_data_using_ocr(dirname):
    pass


def get_table(path):
    table = ocr_api.img_ocr(path)
    table = save_ocr_data._parser(table)
    return table


if __name__ == '__main__':
    dirname = 'static/车库建筑设计规范'
    get_all_data(dirname)



