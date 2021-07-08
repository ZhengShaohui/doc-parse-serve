#!/usr/bin/env python
import os,sys
import json
import time


s = '2018-02-03 14:36:01'
res = time.strptime(s,"%Y-%m-%d %H:%M:%S")
print(dir(res))
