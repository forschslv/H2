from collections import Counter
from typing import Literal

from init_data1 import get_data_by_time, pd
def get_stat_by_tt(tour, typee: Literal['winners', 'half-winners', 'all-winners', 'all', 'participants'] = 'all'):
    data = get_data_by_time(tour, 300)[["from", "sum"]]
    if typee == 'all':
        stat = dict(Counter(data['from'].to_list()))
    elif typee == 'winners':
        idxmax = int(len(data) * 0.08)
        stat = {}
        for idx, i in data.iterrows():
            if idx > idxmax:
                break
            stat[i['from']] = stat.get(i['from'], 0) + 1
    elif typee == 'all-winners':
        idxmax = int(len(data) * 0.45)
        stat = {}
        for idx, i in data.iterrows():
            if idx > idxmax:
                break
            stat[i['from']] = stat.get(i['from'], 0) + 1
    elif typee == 'half-winners':
        idxskip = int(len(data) * 0.08)
        idxmax = int(len(data) * 0.45)
        stat = {}
        for idx, i in data.iterrows():
            if idx > idxmax:
                break
            if idx <= idxskip:
                continue
            stat[i['from']] = stat.get(i['from'], 0) + 1
    elif typee == 'participants':
        idxskip = int(len(data) * 0.45)
        stat = {}
        for idx, i in data.iterrows():
            if idx <= idxskip:
                continue
            stat[i['from']] = stat.get(i['from'], 0) + 1
    else:
        print(f'\033[101m{tour= } | {typee= }\033[0m')
        stat = {}
    return stat

def render_table_stat(data: dict):
    table = '<table>'
    head = '<thead><tr><th>Место</th><th>Регион</th><th>Количество</th></tr></thead>'
    body = '<tbody>'
    i = 1
    for k,v in sorted(data.items(), key=lambda x: (-x[1], x[0])):
        row_html = f'<tr><td>{i}</td><td>{k}</td><td>{v}</td></tr>\n'
        i += 1
        body += row_html
    body += '</tbody>'
    table += head + body + '</table>'
    return table
if __name__ == '__main__':
    print(get_stat_by_tt(1, 'all'))