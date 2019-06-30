# coding=utf-8
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import datetime
import time
import pytz
import random

import os
from os import path
from dash_d3cloud import WordCloud
#from WordCloud import WordCloud

#import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
import base64

from collections import Counter

from matplotlib.colors import LinearSegmentedColormap
from dash.dependencies import Input, Output

from data_input import *

data = get_compound_data()
stopwords = get_stopwords()
stopwords_counter = Counter({a: 10e8 for a in list(stopwords) + ["[", "-"]}) + Counter({a.capitalize(): 10e8 for a in list(stopwords) + ["[", "-"]})
print(stopwords_counter)

colormaps = {'ac24': ["#666666","#333333","#3A4D5A","#000000", "#3A4D5A","#18272E","#1A2126","#1B2228","#213740","#3A4D5A","#869CAD","#869CAD","#65B6F0","#1A2126"],
'aktualne': [ "#F2F2F2","#0485A5","#FAFAFA","#2785A5","#1B5E75","#F44336","#379CBD","#CA372C","#000000","#E8E8E8","#EEEEEE","#2783A3","#E2E2E2","#EDEDED","#333333","#FCFCFC","#F4F4F4","#999999","#00B77D","#04BADF","#E1E1E1","#4A4A4A","#C9372B","#2784A4","#155D76","#E9E9E9","#C5C5C5","#3B5998","#4099FF","#3594B3","#424242","#F34336","#F24335","#E5E5E5","#F5F5F5","#2783A3","#1B5E75","#03677F","#E33D31","#F5F5F3","#FFF8F7","#2785A5","#40B3DA","#F7F7F7","#F4F4F2","#535353","#222222","#2785A5","#000000","#444444","#333333","#2A78A2","#747474","#52A4DE","#666666","#878787","#595959","#888888","#1B5E75","#2783A3","#FF253E","#EEEEEE","#555555","#C9372B","#2784A4","#4A4A4A","#0084B4","#3B5998","#999999"],
'blesk': [ "#16212D","#FF0000","#E9EFF4","#DEE6EE","#EB0000","#5C6773","#CAD5DF","#888888","#91C837","#FE60B2","#1E1E1E","#777777","#D01A1B","#E0E8EB","#FF0000","#16212D","#E9EFF4","#F4F6F7","#B9C7CD","#00B373","#FF5A00","#DEE6EE","#3CC3DC", "#5C6773","#DC0032","#99A4AA","#B469F5","#00C8BE","#6E78DC","#F7B135","#23AAFF","#91C837","#FE60B2","#FF7300","#16212D","#FF0000","#98A3AF","#99A4AA","#707B87","#E9EFF4","#3B4548","#00482E","#333F48","#23AAFF","#00B373","#848F9B","#B469F5","#540101","#F7B135","#FE60B2","#343F4B","#6E78DC","#91C837","#355401","#000000","#191E56","#5C6773","#CAD5DF","#00C8BE","#362A13","#424E56","#3CC3DC","#004754","#3A016B","#004D49","#694506","#053D60","#6D0139","#AB4D00","#C0CED5","#FF5A00","#FF7300","#DC0032","#A9B6EB","#626161","#505A65","#666666","#252525","#2A3440","#7323EB","#AC7279","#B6C1CC","#323232","#A7B3C3","#D01A1B","#827D78","#1C3C7F","#4B141B","#979BA0"],
'parlamentnilisty': ["#EEEEEE", "#000000", "#8CE19B", "#FF7F7F", "#BCBCBC", "#094452", "#0E6A80", "#F5F5F5", "#FCF8E3", "#DFF0D8", "#F2DEDE", "#EEEEEE", "#D9EDF7", "#5CB85C", "#5BC0DE", "#F0AD4E", "#D9534F", "#E6E6E6", "#D0E9C6", "#C4E3F3", "#FAF2CC", "#EBCCCC", "#D4D4D4", "#052932", "#398439", "#269ABC", "#D58512", "#AC2925", "#000000", "#923901", "#449D44", "#31B0D5", "#EC971F", "#C9302C", "#444444", "#0E0E0E", "#E7E7E7", "#3C763D", "#31708F", "#8A6D3B", "#A94442", "#0C5B6E", "#339933", "#329532", "#CC0000", "#C70000", "#E8E8E8", "#DDDDDD", "#8D3701", "#1C7083", "#08404D", "#5F2501", "#5A2301", "#333333", "#C1E2B3", "#AFD9EE", "#F7ECB5", "#E4B9B9", "#E5E5E5", "#C3C3C3", "#7E3101", "#962D00", "#EEA43B", "#D34541", "#53AD53", "#EBEB00", "#97D9E7", "#186272","#DDDDDD", "#333333", "#555555", "#000000", "#3C763D", "#8A6D3B", "#A94442", "#923901", "#0E6A80", "#0088CC", "#CCCCCC", "#31708F", "#444444", "#4D4D4D", "#0C5B6E", "#06313B", "#2B542C", "#245269", "#66512C", "#843534", "#D9534F", "#6BD5EF", "#094452", "#262626", "#3C3C3C", "#A8DFEB", "#993B00", "#FF6500" ],
'sputnik': ["#E0E0E0","#000000","#626262","#212121","#333333","#272727","#383838","#EFEFEF","#333333","#CCCCCC","#FF9933","#990000","#888888","#666666","#999999","#BDBDBD" ],
'protiproud': ["#BBBBBB","#999999","#222222","#BB0000"],
'stredoevropan': ["#4DB2EC","#FAFAFA","#D17646","#F8F8F8","#D760B7","#0016BE","#000000","#CCCCCC","#444444","#F4D03F","#222222","#5472D2","#7C93DD","#00C1CF","#00919C","#FE6C61","#FE9B94","#8D6DC4","#A991D3","#4CADC9","#73BFD5","#CEC2AB","#E1D9CB","#50485B","#695F77","#75D69C","#9CE2B8","#2A2A2A","#EBEBEB","#D2D2D2","#F7BE68","#FAD398","#5AA1E3","#86BAEA","#6DAB3C","#87C456","#F4524D","#F7817D","#F79468","#FAB698","#B97EBB","#CB9FCD","#E6E6E6","#EEEEEE","#FBFBFB","#F3F3F3","#282828","#BABABA","#F7F7F7","#313B45","#54A3DB","#023C8C","#00AC81","#B0B43B","#68C9E8","#333333","#AAAAAA","#4DB2EC","#222222","#000000","#EBEBEB","#2A2A2A","#00AEF0","#5CB85C","#5BC0DE","#F0AD4E","#D9534F","#75D69C","#5472D2","#00C1CF","#FE6C61","#8D6DC4","#4CADC9","#CEC2AB","#50485B","#F7BE68","#5AA1E3","#6DAB3C","#F4524D","#F79468","#B97EBB","#F7F7F7","#444444","#E6E6E6","#0089BD","#449D44","#31B0D5","#EC971F","#C9302C","#FCFCFC","#333333","#F0F0F0","#0088CC","#FF9900","#FF675B","#6AB165","#58B9DA","#555555","#111111","#F5F5F5","#161616","#F1F1F1","#3C5ECC","#00A4B0","#FE5043","#7C57BB","#39A0BD","#C3B498","#413A4A","#5DCF8B","#1B1B1B","#DCDCDC","#F5B14B","#4092DF","#5F9434","#F23630","#F57F4B","#AE6AB0","#414141","#151515","#E8E8E8","#516EAB","#29C5F6","#EB4026","#EAEAEA","#3558C8","#009BA6","#FE4638","#7650B8","#3799B5","#BFAF91","#3C3644","#56CD85","#F5AD41","#378DDD","#5A8D31","#F22D27","#F57941","#AB63AD","#D7D7D7","#E3E3E3","#0074AD","#006DA3","#3FAFD4","#37ABD3","#59A453","#559D50","#E08700","#D68100","#FF4B3C","#FF4132","#464646","#CA212A","#F9F9F9","#7C93DD","#00919C","#FE9B94","#A991D3","#73BFD5","#E1D9CB","#695F77","#9CE2B8","#D2D2D2","#FAD398","#86BAEA","#87C456","#F7817D","#FAB698","#CB9FCD","#0077B3","#E68A00","#FF4F42","#5AA855","#43B0D5","#484848","#417096","#FF6600","#FF5419","#006599","#E14E42","#383838","#919191","#009688","#F3F4F5","#AED13B","#9EC02D","#7D7D7D","#E5E5E5","#7BBF6A","#F54200","#0266A0","#3E5A70","#179CDE","#EE4813","#4C75A3","#00B900","#5D54A4","#EC4D4D","#E9FBE5","#E7F5FE","#FCF0EF","#56B0EE","#1BBC9B","#FCB53F","#FF7877","#67CCE0","#9AD36A","#F9CF79","#EF8495","#0074CC","#49AFCD","#5BB75B","#FAA732","#DA4F49","#428BCA","#DDDDDD","#DEEA4B","#F7F7F7","#F2F2F2","#4DB2EC","#000000","#666666","#222222","#999999","#444444","#333333","#555555","#777777","#111111","#5E5E5E","#EBEBEB","#2A2A2A","#7D7D7D","#5472D2","#595959","#4B4B4B","#00C1CF","#FE6C61","#8D6DC4","#4CADC9","#CEC2AB","#50485B","#75D69C","#F7BE68","#5AA1E3","#6DAB3C","#F4524D","#F79468","#B97EBB","#AAAAAA","#545454","#68C9E8","#B3B3B3","#2B2B2B","#262626","#CCCCCC","#858585","#DDDDDD","#C3C3C3","#555D66","#888888","#AED13B","#5E7F96","#9D9D9E","#F1831E","#21759B","#009688","#EEEEEE","#A5A5A5","#FF7A7A","#1E8CBE","#6C7781","#00AEF0","#5CB85C","#5BC0DE","#F0AD4E","#D9534F","#364A8A","#085B61","#D82E21","#5E4A81","#366A79","#978258","#1E1B22","#3E8E5E","#C3811C","#2A6194","#3E562B","#A3231F","#C3501C","#886389","#56B0EE","#1BBC9B","#9D8967","#FCB53F","#A85959","#FF7877","#31708F","#67CCE0","#3C763D","#9AD36A","#8A6D3B","#F9CF79","#A94442","#EF8495","#73C7E3","#516EAB","#29C5F6","#EB4026","#CA212A","#B5B5B5","#5A5A5A","#2E4453","#40464D","#F8F9F9","#FFA900","#EA4C89","#3B5998","#FF0084","#DD4B39","#3F729B","#CE2127","#007BB6","#CB2027","#F36F24","#FF5500","#32506D","#00ACED","#5289CC","#BB0000","#243442","#4868CF","#0088CC","#C9D2F0","#D3F5F1","#FCDBD7","#E1D5F5","#D0EDF5","#F7F3EB","#E2DDEB","#E1F5E9","#FAF0E1","#DCE9F5","#E5F2DA","#FCE2E1","#F7E1D7","#F4DFF5","#D9D9D9","#F9F9F9","#F3F3F3","#C1C1C1","#7BBF6A","#F54200","#0266A0","#3E5A70","#179CDE","#EE4813","#4C75A3","#00B900","#5D54A4","#B4B4B4","#E53935","#66BB6A","#29B6F6","#7F8FA9","#FDD835","#2BA1CB"]
}                


def create_WC_data(source, start_date, stop_date):
#     # Read the whole text.
    #print(data[data["source"]==source].head())
    text = data[(data["source"]==source) & (data["parsed_date"] > start_date) & (data["parsed_date"] < stop_date)]

    c = Counter("".join(text["title"].values).split()) - stopwords_counter
    output = [{"text": a, "value":b} for a, b in c.most_common(100)]
    
    #print(output)
    return output
    
#     colors = colormaps.get(source, ["#000000", "#111111", "#101010", "#121212", "#212121", "#222222"])
#     cmap = LinearSegmentedColormap.from_list("mycmap", colors)

#     # Generate a word cloud image
#     wc = WordCloud(background_color="white", stopwords=stopwords, 
#                    width=800, height=600, colormap=cmap).generate(text)
#     plt.imshow(wc, interpolation='bilinear')
#     plt.axis("off")
#     return wc

def month_delta(dt, delta, day=None):
    if day is None:
        day = dt.day
    if delta > 0:
        if dt.month == 12:
            return datetime.datetime(dt.year + 1, 1, day)
        else:
            return datetime.datetime(dt.year, dt.month +1, day)
    elif delta < 0:
        if dt.month == 1:
            return datetime.datetime(dt.year - 1, 12, day)
        else:
            return datetime.datetime(dt.year, dt.month - 1, day) 
    else:
        return dt

def create_date_slider(data_series):
    timestamps = data_series.apply(lambda x: int(x.timestamp()))
    min_ts = int(np.min(timestamps))
    max_ts = int(np.max(timestamps))
    min_d = datetime.datetime.fromtimestamp(min_ts)
    max_d = datetime.datetime.fromtimestamp(max_ts)
    start_range = month_delta(min_d, 1, day=1)    
    stop_range = month_delta(max_d, -1, day=1)
    marks = {}
    current_date = start_range
    counter = 0
    while current_date != stop_range:
        if counter % 6 == 0:
            marks.update({int(datetime.datetime.timestamp(current_date)): {
                'label': current_date.strftime("%d.%m.%Y"),
                'style': {"transform": "rotate(45deg)"}}})
        current_date = month_delta(current_date, 1)
        counter += 1
    return min_ts, max_ts, marks

app_iplot = dash.Dash()
server = app_iplot.server

min_ts, max_ts, marks = create_date_slider(data["parsed_date"])

app_iplot.layout = html.Div([
    html.Div([dcc.RangeSlider(
        id='date_range',
        min=min_ts,
        max=max_ts,
        value=[min_ts, max_ts],
        marks=marks   
    )], style ={'margin-bottom': '60px'}),
    html.Div(id="date-range-out", style={'textAlign': "center"}),
    html.Div([
    html.Div([
    dcc.Dropdown(
        id='source_input1',
        options=[{'label': x, 'value': x} for x in np.unique(data.source.values)],            
        value="ac24"
    ),
    html.Div([
        WordCloud(id="cur_plot1", words=[{"text":"", "value":0}])
        ], id='plot_div1')
    ], style={'width': '49%', 'display':'inline-block'}),
    html.Div([
    dcc.Dropdown(
        id='source_input2',
        options=[{'label': x, 'value': x} for x in np.unique(data.source.values)],            
        value="blesk"
    ),
    html.Div([WordCloud(id = 'cur_plot2',  words=[{"text":"", "value":0}]),
        ], id='plot_div2')
    ], style={'width': '49%', 'display':'inline-block'})
    ])
])

def get_data_for_range_and_source(source, date_range):
    dates = [pytz.utc.localize(datetime.datetime.fromtimestamp(ts)) for ts in date_range]
    data = create_WC_data(source, *dates)
    return data

@app_iplot.callback(Output(component_id='date-range-out', component_property='children'),
                    [Input(component_id = 'date_range', component_property='value')])
def update_date_range(date_range):
    return "From {} to {}".format(*[datetime.datetime.fromtimestamp(x).strftime("%d. %B %Y") for x in date_range])          

@app_iplot.callback(
    Output(component_id='cur_plot1', component_property='words'),
    [Input(component_id='source_input1', component_property='value'),
     Input(component_id = 'date_range', component_property='value')]
)
def update_graph1(source, date_range):
    return get_data_for_range_and_source(source, date_range)

@app_iplot.callback(
    Output(component_id='cur_plot2', component_property='words'),    
    [Input(component_id='source_input2', component_property='value'),
     Input(component_id = 'date_range', component_property='value')]
)
def update_graph2(source, date_range):
    return get_data_for_range_and_source(source, date_range)

if __name__ == '__main__':
#    app_iplot.run_server(debug=True, host="0.0.0.0")
   app_iplot.run_server(host="0.0.0.0")
 
