#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
import base64
import time
import json

from urllib.parse import urlparse
import traceback
import requests
import base64


def img_ocr(img_filename):
    def get_img_base64(img_file):
        with open(img_file, 'rb') as infile:
            s = infile.read()
            t = base64.b64encode(s)
            t = str(t, 'utf-8')
            return t

    url = 'http://172.18.50.20:18090/tuling/uocr/v2/base64/001'
    try:
        f = open(img_filename, 'rb')
        img = base64.b64encode(f.read())
        data = {'base64': img, 'category': 'ch_en'}
        response = requests.post(url, data=data)
        res = json.loads(response.text)
        res = json.loads(res['body'])
        res = res['pages'][0]
        return res
    except Exception as e:
        print('Error:', e)
        return {}


def pdf_ocr(img_filename):
    url = 'http://172.18.50.20:18090/tuling/uocr/v2/recognizepi'
    try:
        f = open(img_filename, 'rb')
        data = {
            'trackId': 'pdf',
            'category': 'ch_en'
        }
        files = {'file': open(img_filename, 'rb')}
        response = requests.post(url, data=data, files=files)
        res = json.loads(response.text)
        # res = json.loads(res['body'])
        return res
    except Exception as e:
        print('Error:', e)
        return {}


if __name__ == '__main__':
    # res = pdf_ocr('tmp_test.pdf')
    # print(res)
    res = img_ocr('表7.1.1.jpg')
    print(res)
    tables = res['tables'][0]
    cells = tables['cells'][0]
    lines = cells['lines'][0]
    for item in lines:
        print(item, lines[item])
    pass
