import os
import pdfplumber as pdfp
import pandas as pd
import json
import re


def extract(path):
    tables = []
    pattern = '^表\d.+'
    titles = []
    with pdfp.open(path) as pdf:
        p = 1
        i = 0
        # 按页遍历pdf
        for page in pdf.pages:
            text = page.extract_text()
            text = text.split('\n')
            for item in text:
                item = item.rstrip(' ')
            # 处理每页中的表格
            for table in page.extract_tables():
                # 判断表格是否跨页
                # print(table)
                if compare_list(table[0], text[0].split()):
                    # print(tables[-1][0])
                    tables[-1]['table'].extend(table)
                else:
                    # 添加表头
                    for item in text:
                        if re.match(pattern, item) and item not in titles:
                            titles.append(item)
                            i += 1
                            tables.append({'table': table, 'page': p, 'title': item, 'id': i})
                            break
            titles = []
            p += 1
    return tables


# def to_json(tables):
#     for table in tables:


def compare_list(table, text):
    for item in table:
        if item == '':
            continue
        elif item not in text:
            return False
    return True


def test(path):
    with pdfp.open(path) as pdf:
        page = pdf.pages[4]
        # print(page.extract_text())
        text = page.extract_text().split(' \n')[0].split()
        table = page.extract_tables()
        print(text)
        print(table)


if __name__ == '__main__':
    tables = extract('1.pdf')
    print(tables)
    # for item in tables:
    #     print(item)
    # test('1.pdf')
