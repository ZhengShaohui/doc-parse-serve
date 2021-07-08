#!/usr/bin/env python3
import os, sys
import json
from pprint import pprint

from bim_table import ocr_api

from bim_table.docx_utils import gen_docx


def __get_span(coord):
    # [x_min, x_max, y_min, y_max]
    '''
    x_min, x_max
    y_min
    y_max
    '''
    x_min, x_max, y_min, y_max = 100000, -1, 100000, -1
    for x in coord:
        if x['x'] < x_min:
            x_min = x['x']
        if x['x'] > x_max:
            x_max = x['x']
        if x['y'] < y_min:
            y_min = x['y']
        if x['y'] > y_max:
            y_max = x['y']
    return [x_min, x_max, y_min, y_max]


def _parse_line(lines):
    texts = []
    for line in lines:
        tmp = {}
        tmp['span'] = __get_span(line['coord'])
        content = ''
        for word in line.get('words', []):
            content += word['content']
        tmp['content'] = content
        texts.append(tmp)
    texts = sorted(texts, key=lambda x:x['span'][2])
    return texts


def _parse_table(tables):
    def __parse_cell(cell):
        def _get_content(lines):
            if not lines:
                return ''
            content = ''
            for line in lines:
                for word in line.get('words', []):
                    content += word['content']
            return content

        cell_info = {}
        cell_info['span'] = __get_span(cell['coord'])
        cell_info['index'] = [cell['row'], cell['col']]
        cell_info['cell_span'] = [cell['rowspan'], cell['colspan']]
        cell_info['content'] = _get_content(cell.get('lines', None))
        return cell_info

    result = []
    for table in tables:
        tmp = {}
        tmp['span'] = __get_span(table['coord'])
        tmp['shape'] = [table['rows'], table['cols']]
        tmp['cells'] = []
        for cell in table['cells']:
            cell_info = __parse_cell(cell)
            tmp['cells'].append(cell_info)
        result.append(tmp)
    result = sorted(result, key=lambda x:x['span'][2])
    return result


def _cell_sort(table):
    cells = []
    for i in range(table['shape'][0]):
        row = []
        for j in range(table['shape'][1]):
            row.append('')
        cells.append(row)
    for cell in table['cells']:
        row, col = cell['index']
        cells[row-1][col-1] = cell['content']
    pass


def _fix_table_cell(tables, texts):
    '''
    文本坐标边界与表格/单元格边界比较，修复部分单元格文本为空的情况
    '''
    bias = 1 #坐标误差
    text0 = []
    cell_text = [[] for x in tables]
    for text in texts:
        text_span = text['span']
        flag = False
        for i in range(len(tables)):
            table = tables[i]
            table_span = table['span']
            if text_span[0] >= table_span[0]-bias \
                    and text_span[1] <= table_span[1]+bias \
                    and text_span[2] >= table_span[2]-bias \
                    and text_span[3] <= table_span[3]+bias:
                cell_text[i].append(text)
                flag = True
                break
        if not flag:
            text0.append(text)

    for i in range(len(tables)):
        _texts = cell_text[i]
        table = tables[i]
        for _text in _texts:
            _text_span = _text['span']
            for _cell in table['cells']:
                _cell_span = _cell['span']
                if _text_span[0] >= _cell_span[0]-bias and _text_span[1] <= _cell_span[1]+bias and _text_span[2] >= _cell_span[2]-bias and _text_span[3] <= _cell_span[3]+bias:
                    _cell['content'] += _text['content']
                    break
    return text0, tables


def _parser(page_res):
    texts, tables = [], []
    if 'lines' in page_res:
        texts = _parse_line(page_res['lines'])
    if 'tables' in page_res:
        tables = _parse_table(page_res['tables'])
        texts, tables = _fix_table_cell(tables, texts)
    result = []
    for x in texts:
        x['type'] = 'text'
        result.append(x)
    for x in tables:
        x['type'] = 'table'
        result.append(x)
    result = sorted(result, key=lambda x:x['span'][2])

    return result


def convert():
    rootdir = 'table_images'
    for dirname in os.listdir(rootdir):
        data = []
        for filename in os.listdir(os.path.join(rootdir, dirname)):
            if '表' in filename:
                item = {}
                img_file = os.path.join(os.path.join(rootdir, dirname), filename)
                #print(img_file)
                res = ocr_api.img_ocr(img_file)
                res = _parser(res)
                item['filename'] = img_file
                item['data'] = res
                data.append(item)
        gen_docx(data, os.path.join('table_docx', dirname))
        print(dirname)
    with open('all_ocr_data.json', 'w') as f:
        for item in data:
            item_str = json.dumps(item, ensure_ascii=False)
            f.write(item_str+'\n')
    



if __name__ == '__main__':
    # convert()
    # res = ocr_api.img_ocr('表7.1.1.jpg')
    # res = _parser(res)
    # print(res)
    pass
