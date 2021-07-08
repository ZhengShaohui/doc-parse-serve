#!/usr/bin/env python3
import os,sys
from pprint import pprint

from docx_utils import gen_docx, load_docx


def load():
    rootdir = 'table_docx'
    save_dir = 'table_docx_fix'
    for filename in os.listdir(rootdir):
        if filename in ['智能建筑设计标准.docx', '消防给水及消火栓系统技术规范.docx']:
            continue
        if filename != '住宅设计规范.docx':
            continue
        print(filename)
        res = load_docx(os.path.join(rootdir, filename))
        gen_docx(res, os.path.join(save_dir, filename))


if __name__ == '__main__':
    load()
    pass
