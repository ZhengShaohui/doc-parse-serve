import re


def is_table(item):
    pattern = '<table>(.+)</table>'
    txt = item[0]
    if re.match(pattern, txt):
        return True
    return False