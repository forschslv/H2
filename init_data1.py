from collections import Counter
from typing import Literal

import pandas as pd
from bs4 import BeautifulSoup

def raisee(e: BaseException):
    raise e
def get_data_by_time(tour, time):
    if tour == 1:
        data = pd.DataFrame(columns=['place', 'name', 'from', 'class', '1', '2', '3', '4', 'sum'])
    else:
        data = pd.DataFrame(columns=['place', 'name', 'from', 'class', '1', '2', '3', '4', '5', '6', '7', '8', 'sum'])
    with open(f"Материалы/{'Первый тур' if tour == 1 else ('Второй тур' if tour == 2 else raisee(ValueError('tour should be 1 or 2')))}/{time}.html") as f:
        text = f.read()
    soup = BeautifulSoup(text, 'html.parser')
    skip = 2
    for i in soup.find_all(name='tr'):
        if skip:
            skip -= 1
            continue
        try:
            name_from_class = i.find(name='td', attrs={'class': "party"}).text
        except Exception as e:
            print('\033[93m' + repr(e) + '\033[0m')
            continue

        name = ' '.join(name_from_class.split()[:3])
        from_ = name_from_class[name_from_class.find('(') + 1: name_from_class.find(',')]
        class_ = name_from_class[name_from_class.find(',') + 1: name_from_class.find('класс')]

        zad = []
        sm = 0
        for j in i.find_all(name='td', attrs={'class': 'ioiprob'}):
            if j.text.strip() == '.':
                zad.append(0)
            else:
                zad.append(int(j.text))
                sm += zad[-1]
        row = {'place': [i.find(name='td', attrs={'class': "rankl"}).text],
               'name': [name],
               'from': [from_],
               'class': [class_],
               **{str(i1 + 1): zad[i1] for i1 in range(len(zad))},
               'sum': [sm]}
        data = pd.concat([data,
                          pd.DataFrame(row)],
                         axis=0)
    print(data)
    return data


def render_table_by_df(data):
    table = '<table>'
    head = '<thead><tr>'
    cols = data.columns
    for i in cols:
        head += f"<th>{i}</th>"
    head += '</tr></thead>'

    body = '<tbody>'
    for idx, irow in data.iterrows():
        row_html = '<tr>'
        for col in cols:
            row_html += f'<td>{irow[col]}</td>'
        row_html += '</tr>\n'
        body += row_html
    body += '</tbody>'
    table += head + body + '</table>'
    return table
def render_table(tour, time):
    data = get_data_by_time(tour, time)
    return render_table_by_df(data)
# print(get_data_by_time(120))


moscow = pd.read_csv("Материалы/Результаты регионального этапа в Москве.csv", sep=';', encoding = 'windows-1251')
piter = pd.read_csv("Материалы/Результаты регионального этапа в Санкт-Петербурге.csv", sep=';', encoding = 'windows-1251')

psch = []
for _, i in piter[['Участник']].iterrows():
    qweq = str(i["Участник"])
    qweq = qweq[qweq.find('(') + 1: qweq.find(')')]
    qweq = qweq[:qweq.rfind(',')]
    psch.append(qweq)
def render_table_reg(typee: Literal['winners', 'half-winners', 'all-winners', 'all', 'participants']):
    print(typee)
    data = pd.concat([moscow[["Школа"]],
                      pd.DataFrame({"Школа": psch})],
                         axis=0)

    if typee == 'all':
        stat = dict(Counter(data['Школа'].to_list()))
    elif typee == 'winners':
        idxmax = int(len(data) * 0.08)
        stat = {}
        cnt = 1
        for idx, i in data.iterrows():
            if cnt > idxmax:
                break
            cnt += 1
            stat[i['Школа']] = stat.get(i['Школа'], 0) + 1
    elif typee == 'all-winners':
        idxmax = int(len(data) * 0.45)
        stat = {}
        cnt = 1
        for idx, i in data.iterrows():
            if cnt > idxmax:
                break
            cnt += 1
            stat[i['Школа']] = stat.get(i['Школа'], 0) + 1
    elif typee == 'half-winners':
        idxskip = int(len(data) * 0.08)
        idxmax = int(len(data) * 0.45)
        stat = {}
        cnt = 0
        for idx, i in data.iterrows():
            cnt += 1
            if cnt > idxmax:
                break
            if cnt <= idxskip:
                continue
            stat[i['Школа']] = stat.get(i['Школа'], 0) + 1
    elif typee == 'participants':
        cnt = 0
        idxskip = int(len(data) * 0.45)
        stat = {}
        for idx, i in data.iterrows():
            cnt += 1
            if cnt <= idxskip:
                continue
            stat[i['Школа']] = stat.get(i['Школа'], 0) + 1
    else:
        print(f'\033[101m{typee= }\033[0m')
        stat = {}
    print(stat)
    return stat




def render_table_stat_reg(data: dict):
    table = '<table>'
    head = '<thead><tr><th>Место</th><th>Школа</th><th>Количество</th></tr></thead>'
    body = '<tbody>'
    i = 1
    lasti = 1
    last = 0
    vls = tuple(data.values())
    cnt = 0
    for k, v in sorted(data.items(), key=lambda x: (-x[1], x[0])):
        if last != v:
            lasti = i
            last = v
            cnt = vls.count(v)
        if cnt <= 1:
            row_html = f'<tr><td>{i}</td><td>{k}</td><td>{v}</td></tr>\n'
        else:
            row_html = f'<tr><td>{lasti}-{lasti + cnt - 1}</td><td>{k}</td><td>{v}</td></tr>\n'
        i += 1
        body += row_html
    body += '</tbody>'
    table += head + body + '</table>'
    return table

print(moscow.columns)
print(piter.columns)