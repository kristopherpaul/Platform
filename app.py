from flask import Flask, render_template, request, jsonify
import json

import pandas as pd
from technical import *
import datetime
papadata = pd.read_csv('NIFTNEAR.csv')
papadata['time'] = papadata['time'].apply(lambda x: "0" * (4 - len(str(x))) + str(x))
papadata['time'] = papadata['time'].apply(lambda x: f"{x[0:2]}:{x[2:]}")
papadata['date'] = papadata['date'] + ' ' + papadata['time']
date_format = "%d-%m-%y %H:%M"
papadata['date'] = (papadata['date'].apply(lambda x: datetime.datetime.strptime(x, date_format).replace(tzinfo=None)))
data = TimeMatrix(papadata)

expavg = xavg(data.close, 65)
high = highest(data.high, 10)
low = lowest(data.low, 10)


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def strategy_builder():
    if request.method == "POST":
        exec(request.get_data().decode("utf-8"))
        df = pd.read_csv("strategy_output.csv")
        ret = json.dumps({"x":df.x.values.tolist(),"y":df.y.values.tolist()})
        return ret
    return render_template('dashboard.html')

@app.route('/login')
def login():
    return render_template('sign-in.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=False)