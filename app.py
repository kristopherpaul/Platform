from flask import Flask, render_template, request, jsonify
import json
#from langchain_openai.chat_models import ChatOpenAI
#from langchain.schema import HumanMessage
import cohere

import pandas as pd
from technical import *
from language import *
import datetime
papadata = pd.read_csv('NIFTNEAR.csv')
papadata['time'] = papadata['time'].apply(lambda x: "0" * (4 - len(str(x))) + str(x))
papadata['time'] = papadata['time'].apply(lambda x: f"{x[0:2]}:{x[2:]}")
papadata['date'] = papadata['date'] + ' ' + papadata['time']
date_format = "%d-%m-%y %H:%M"
papadata['date'] = (papadata['date'].apply(lambda x: datetime.datetime.strptime(x, date_format).replace(tzinfo=None)))
data = OHLC(papadata)
data_timestamps = list(map(lambda x: pd.to_datetime(x).strftime("%Y-%m-%d %H:%M:%S"),data.time.tolist()))

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def strategy_builder():
    if request.method == "POST":
        extra_code = """
test = Backtest(long, short, data)
test.run()
cumpnl = [0]
lot = 50 # lot size of nifty in F&O market

for i in range(len(test.timestamps) - 1):
    pnl = test.exitprice[i] - test.entryprice[i]
    pnl *= lot
    if test.signal[i] == 'sell':
        pnl *= -1
    cumpnl.append(cumpnl[-1] + pnl)

test.timestamps = list(map(lambda x: pd.to_datetime(x).strftime("%Y-%m-%d %H:%M:%S"),test.timestamps))
"""
        full_code = request.get_data().decode("utf-8")+extra_code
        exec(full_code,globals())
        ret = json.dumps({"timestamps":test.timestamps,"cumpnl":cumpnl,"signal":test.signal,"entryprice":test.entryprice,"data_timestamps":data_timestamps,"open":data.open._tolist(),"high":data.high._tolist(),"low":data.low._tolist(),"close":data.close._tolist()})
        return ret
    return render_template('dashboard.html')

@app.route('/chat', methods=['GET', 'POST'])
def llm_interact():
    if request.method == "POST":
        message = request.get_data().decode("utf-8")
        co = cohere.Client('D66in2vKC1q6ap86g3xxdVbQoOk2ZyaKCNpmjMKB')
        response = co.chat(
            message, 
            model="command", 
            temperature=0.9
        )
        reply = response.text
        #reply = message
        return json.dumps({'message': reply})

@app.route('/login')
def login():
    return render_template('sign-in.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=False)