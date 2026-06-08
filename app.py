from functools import cache

import flask
import pandas as pd
import os
path_to_data = 'data.csv'
from init_data1 import get_data_by_time, render_table_by_df, render_table
from statistics import get_stat_by_tt, render_table_stat

if os.path.exists(path_to_data):
    data = pd.read_csv(path_to_data)
else:
    data = pd.DataFrame()

app = flask.Flask(__name__)



@app.route("/api/get_data/<tour_num>/<time>")
def data_ret(tour_num, time):
    if tour_num not in {'1', '2'}:
        flask.abort(400)
    else:
        if f"{time}.html" not in os.listdir('Материалы/Первый тур' if tour_num == 1 else 'Материалы/Второй тур'):
            flask.abort(404)
        else:
            return get_data_by_time(int(tour_num), time).to_json(index=False, orient='split')

@app.route("/api/get_data_html/<tour_num>/<time>")
def data_ret1(tour_num, time):
    if tour_num not in {'1', '2'}:
        flask.abort(400)
    else:
        if f"{time}.html" not in os.listdir('Материалы/Первый тур' if tour_num == 1 else 'Материалы/Второй тур'):
            flask.abort(404)
        else:
            flask.abort(500, "NOT IMPLEMENTED")



@app.route('/api/get_possible')
@app.route('/api/get_possible/')
@app.route('/api/get_possible/<fs>')
@cache
def possible(fs=None):
    if fs is None:
        f = []
        for i in os.scandir('Материалы/Первый тур'):
            f.append(int(i.name[:i.name.find('.')]))

        s = []
        for i in os.scandir('Материалы/Второй тур'):
            s.append(int(i.name[:i.name.find('.')]))

        return {'1': f,
                '2': s}
    if fs == 1:
        f = []
        for i in os.scandir('Материалы/Первый тур'):
            f.append(int(i.name[:i.name.find('.')]))
        return f
    if fs == 2:
        s = []
        for i in os.scandir('Материалы/Второй тур'):
            s.append(int(i.name[:i.name.find('.')]))
        return s
    flask.abort(400)

@app.route("/")
def index():
    return flask.render_template("index.html")
@app.route("/reg_rat")
def reg_rat():
    args = flask.request.args
    table = render_table_stat(get_stat_by_tt(int((args.get('category', "Первый тур") == "Первый тур") or 2), args.get('stat', 'all')))
    return flask.render_template('reg_rat.html', products=table)
APP_SETTINGS = {
    "site_name": "ХАКАТОН",
    "currency_symbol": "ERROR",
}
@app.context_processor
def inject_settings():
    return dict(cfg=APP_SETTINGS)

@app.route('/reg_rat')
def reg_rat():
    args = flask.request.args
    try:
        table = render_table(int((args.get('category', "Первый тур") == "Первый тур") or 2), int(args.get('q', 0)))
        return flask.render_template('reg_rat.html', products = table)
    except Exception as e:
        print(repr(e))
        text = ''
        if e.__class__ == FileNotFoundError:
            text = "Неверное время тура"
        return flask.render_template('reg_rat.html', products = f"""
        <!-- Empty search catalog fallback state -->
                <div class="text-center py-20 bg-white rounded-2xl border border-neutral-200 shadow-sm max-w-md mx-auto mt-10">
                    <svg class="mx-auto h-12 w-12 text-neutral-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M15.182 15.182a4.5 4.5 0 01-6.364 0M21 12a9 9 0 11-18 0 9 9 0 0118 0zM9.75 9.75c0 .414-.168.75-.375.75s-.375-.336-.375-.75.168-.75.375-.75.375.336.375.75zm-.375 0h.008v.015h-.008V9.75zm5.625 0c0 .414-.168.75-.375.75s-.375-.336-.375-.75.168-.75.375-.75.375.336.375.75zm-.375 0h.008v.015h-.008V9.75z" />
                    </svg>
                    <h3 class="mt-2 text-sm font-semibold text-neutral-900">Ничего не найдено</h3>
                    <p class="mt-1 text-xs text-neutral-500">По вашему запросу во встроенной базе данных данных не обнаружено ({text}).</p>
                    <div class="mt-6">
                        <a href="http://127.0.0.1:5000/catalog?" class="inline-flex items-center px-4 py-2 border border-transparent text-xs font-semibold rounded-xl text-white bg-indigo-600 hover:bg-indigo-700 transition-colors shadow-sm">
                            Сбросить фильтры
                        </a>
                    </div>
                </div>""")

@app.route('/catalog2')
def catalog2():
    args = flask.request.args
    try:
        table = render_table(int((args.get('category', "Первый тур") == "Первый тур") or 2), int(args.get('q', 0)))
        return flask.render_template('catalog2.html', products = table)
    except Exception as e:
        print(repr(e))
        text = ''
        if e.__class__ == FileNotFoundError:
            text = "Неверное время тура"
        return flask.render_template('catalog2.html', products = f"""
        <!-- Empty search catalog fallback state -->
                <div class="text-center py-20 bg-white rounded-2xl border border-neutral-200 shadow-sm max-w-md mx-auto mt-10">
                    <svg class="mx-auto h-12 w-12 text-neutral-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M15.182 15.182a4.5 4.5 0 01-6.364 0M21 12a9 9 0 11-18 0 9 9 0 0118 0zM9.75 9.75c0 .414-.168.75-.375.75s-.375-.336-.375-.75.168-.75.375-.75.375.336.375.75zm-.375 0h.008v.015h-.008V9.75zm5.625 0c0 .414-.168.75-.375.75s-.375-.336-.375-.75.168-.75.375-.75.375.336.375.75zm-.375 0h.008v.015h-.008V9.75z" />
                    </svg>
                    <h3 class="mt-2 text-sm font-semibold text-neutral-900">Ничего не найдено</h3>
                    <p class="mt-1 text-xs text-neutral-500">По вашему запросу во встроенной базе данных данных не обнаружено ({text}).</p>
                    <div class="mt-6">
                        <a href="http://127.0.0.1:5000/catalog?" class="inline-flex items-center px-4 py-2 border border-transparent text-xs font-semibold rounded-xl text-white bg-indigo-600 hover:bg-indigo-700 transition-colors shadow-sm">
                            Сбросить фильтры
                        </a>
                    </div>
                </div>""")

@app.route('/catalog3')
def catalog3():
    args = flask.request.args
    try:
        table = render_table(int((args.get('category', "Первый тур") == "Первый тур") or 2), int(args.get('q', 0)))
        return flask.render_template('catalog3.html', products = table)
    except Exception as e:
        print(repr(e))
        text = ''
        if e.__class__ == FileNotFoundError:
            text = "Неверное время тура"
        return flask.render_template('catalog3.html', products = f"""
        <!-- Empty search catalog fallback state -->
                <div class="text-center py-20 bg-white rounded-2xl border border-neutral-200 shadow-sm max-w-md mx-auto mt-10">
                    <svg class="mx-auto h-12 w-12 text-neutral-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M15.182 15.182a4.5 4.5 0 01-6.364 0M21 12a9 9 0 11-18 0 9 9 0 0118 0zM9.75 9.75c0 .414-.168.75-.375.75s-.375-.336-.375-.75.168-.75.375-.75.375.336.375.75zm-.375 0h.008v.015h-.008V9.75zm5.625 0c0 .414-.168.75-.375.75s-.375-.336-.375-.75.168-.75.375-.75.375.336.375.75zm-.375 0h.008v.015h-.008V9.75z" />
                    </svg>
                    <h3 class="mt-2 text-sm font-semibold text-neutral-900">Ничего не найдено</h3>
                    <p class="mt-1 text-xs text-neutral-500">По вашему запросу во встроенной базе данных данных не обнаружено ({text}).</p>
                    <div class="mt-6">
                        <a href="http://127.0.0.1:5000/catalog?" class="inline-flex items-center px-4 py-2 border border-transparent text-xs font-semibold rounded-xl text-white bg-indigo-600 hover:bg-indigo-700 transition-colors shadow-sm">
                            Сбросить фильтры
                        </a>
                    </div>
                </div>""")
if __name__ == '__main__':
    app.run(
        debug=True,
    )
