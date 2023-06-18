import numpy as np
import pandas as pd
import yfinance as yf
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import streamlit as st
basedailydata = yf.download(tickers = 'EURUSD=X' ,period ='1d', interval = '1d')
#print(basedailydata)
maindate=basedailydata.first('1d')

fig = go.Figure()
fig = make_subplots(rows = 1,cols = 1)
fig.update_layout(title_text="title", margin={"r": 0, "t": 0, "l": 0, "b": 0}, height=1100)
asset=pd.DataFrame({'pair':['EURUSD=X','GBPUSD=X','JPYUSD=X','AUDUSD=X','CADUSD=X','CHFUSD=X','NZDUSD=X' ],
       'pipvalue':[0.0001,0.0001,0.000001,0.0001,0.0001,0.0001,0.0001],
        'incolor':['lime','green','aqua','magenta','yellow','turquoise','coral'] ,          
        'dwcolor':['red','orange','dimgrey','blue','purple','indigo','black']})
asset = asset.reset_index()

df = pd.DataFrame({'c1': [10, 11, 12], 'c2': [100, 110, 120]})
df = df.reset_index()

stats=pd.DataFrame()

for index, row in asset.iterrows():
    a=row['pair']
    b=row['pipvalue']
    
    dailydata = yf.download(tickers = a ,period ='1d', interval = '5m')
    ailydata =dailydata[dailydata.index.date==maindate.index.date]
    ddata=dailydata[dailydata.index.hour+dailydata.index.minute==0]
    dailydata["cOpen"]=dailydata.apply(lambda x: x["Open"]/b-ddata["Open"]/b, axis=1)
    dailydata["cHigh"]=dailydata.apply(lambda x: x["High"]/b-ddata["Open"]/b, axis=1)
    dailydata["cLow"]=dailydata.apply(lambda x: x["Low"]/b-ddata["Open"]/b, axis=1)
    dailydata["cClose"]=dailydata.apply(lambda x: x["Close"]/b-ddata["Open"]/b, axis=1)
    fig.add_trace(go.Candlestick(x=dailydata.index,
        open=dailydata['cOpen'],
        high=dailydata['cHigh'],
        low=dailydata['cLow'],
        close=dailydata['cClose'], name = a,increasing_line_color= row['incolor'], decreasing_line_color= row['dwcolor']))  
    #print(dailydata['cHigh'].max())
    temp = pd.DataFrame({'pair':[a],
                         'day_high':[round(dailydata['cHigh'].max())] ,
                         'day_low':[round(dailydata['cLow'].min())],
                         'day_range':[round(dailydata['cHigh'].max()-dailydata['cLow'].min())],
                         'current_time':pd.to_datetime(dailydata.index[-1]),#dailydata.index[-1].year,dailydata.index[-1].day,dailydata.index[-1].day,
                         'current_price':dailydata[dailydata.index==dailydata.index[-1]]['cClose'].values.round(0)
    })
    stats = pd.concat([stats, temp])

st.set_page_config(layout="wide")     
col1, col2 = st.columns([2, 0.8])
stats=stats.sort_values(by='current_price',key=abs,ascending=False)
col2.table(stats)
col1.plotly_chart(fig,use_container_width=True)
