import re


def is_table(item):
    pattern = '<table>(.+)</table>'
    txt = item[0]
    if re.match(pattern, txt):
        return True
    return False


def tran_data(table):
    cell_data = []
    sheet = {'celldata': [], 'merge': {}, 'title': []}
    span = []
    title = []
    start_r = 0
    merge = {}
    shape = [0, 0]
    k = 0
    for item in table:
        if 'content' in item:
            title.append(item['content'])
        if 'cells' in item:
            res = trans_table(item, start_r)
            cell_data.extend(res[0])
            span.extend(res[2])
            start_r = start_r + res[1][0]
            if k == 0:
                shape = res[1]
            else:
                shape[0] += res[1][0]
            k += 1
    for i in range(len(cell_data)):
        r = cell_data[i]['r']
        c = cell_data[i]['c']
        merge[str(r) + '_' + str(c)] = {'r': r, 'c': c, 'rs': span[i][0], 'cs': span[i][1]}
    sheet['celldata'] = cell_data
    sheet['merge'] = merge
    sheet['title'] = title
    sheet['shape'] = shape
    return sheet


def trans_table(data, start_r):
    cell_data = []
    span = []
    cells = data['cells']
    shape = data['shape']
    print(shape)
    for item in cells:
        content = item['content']
        index = item['index']
        span.append(item['cell_span'])
        r = index[0] +start_r -1
        c = index[1] -1
        cell_data.append({'r': r, 'c': c, 'v': content})
    return [cell_data, shape, span]