#!/usr/bin/python3

# Read flow levels and calculate liquifier He production rate
# Derek Fujimoto
# Oct 2024

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
from scipy.optimize import curve_fit
import mpld3
import plotly.express as px
import plotly.graph_objs as go

import warnings
warnings.simplefilter('ignore')
from ucnhistory import ucnhistory

# times in minutes
total_time=60*6
window_size = 10

labels = {'ucn2_he4_lvl204_rdlvl_measured': 'MD Level (lvl204)',
          'ucn2_he4_lvl203_rdlvl_measured': '4K Pot Level (lvl203)',
          'ucn2_he4_lvl202_rdlvl_measured': '1K Pot Level (lvl202)',
          'ucn2_he4_fm207_rdflow_measured': 'Return Flow (fm207)'
          }

# tables to load: level readings
levels = [{'table': 'ucn2epicsothers_measured',
           'columns':['ucn2_he4_lvl204_rdlvl_measured',     # MD
                      'ucn2_he4_lvl203_rdlvl_measured']},   # 4K pot
          {'table': 'ucn2epicsphase2b_measured',
           'columns':['ucn2_he4_lvl202_rdlvl_measured']}    # 1K pot
         ]

# conversions to liquid L
conv = {'ucn2_he4_lvl204_rdlvl_measured': 12.6,
        'ucn2_he4_lvl203_rdlvl_measured': 2.5834,
        'ucn2_he4_lvl202_rdlvl_measured': 0.4519,
        }
conv = pd.Series(conv)

# get now minus 1h
t0 = datetime.datetime.now() - datetime.timedelta(minutes=total_time)

# read levels data
hist = ucnhistory()

df_list = []
for lvl in levels:
    df_list.append(hist.get_data(**lvl, start=str(t0)).set_index('epoch_time'))

df_lvl = pd.concat(df_list, axis='columns')
df_lvl *= conv

# read the flows in liquid L/min
df_flw =  hist.get_data(table = 'ucn2epicsothers_measured',
                        columns = ['ucn2_he4_fm207_rdflow_measured'],
                        start=str(t0)).set_index('epoch_time')
df_flw /= 745

def get_prod_rate(df_lvl, df_flw):

    # fit columns with linear line
    fn = lambda x, a, b: a*x+b

    slopes = {}

    # draw and get slopes
    for col in df_lvl.columns:
        x = df_lvl.index
        y = df_lvl[col]

        par, cov = curve_fit(fn, x, y)
        std = np.diag(cov)**0.5
        slopes[col] = par[0]*60 # L/min
        slopes[f'd{col}'] = std[0]*60 # L/min

    # convert to series
    slopes = pd.Series(slopes)
    slopes.name = np.mean(x)

    # add in flow
    slopes['ucn2_he4_fm207_rdflow_measured'] = df_flw.mean().values[0]
    slopes['ducn2_he4_fm207_rdflow_measured'] = df_flw.std().values[0]

    return slopes

idx_start = df_lvl.index[0]
idx_stop = idx_start + window_size*60

rates = []
while idx_stop <= df_lvl.index[-1]:
    rates.append(get_prod_rate(df_lvl.loc[idx_start:idx_stop], df_flw.loc[idx_start:idx_stop]))
    idx_start = idx_stop
    idx_stop = idx_start + window_size*60

rates = pd.concat(rates, axis='columns').transpose()*60
rates.rename(columns=labels, inplace=True)
rates.rename(columns={f'd{key}':f'd{label}' for key, label in labels.items()}, inplace=True)

prod_rate = rates[[col for col in rates if 'd' != col[0]]].sum(axis='columns')
dprod_rate = (rates[[col for col in rates if 'd' == col[0]]]**2).sum(axis='columns')**0.5

# get time in current timezone
x = pd.to_datetime(rates.index.values, unit='s').tz_localize('UTC').tz_convert('America/Vancouver')

data = []
for col in rates:
    if 'd' == col[0]: continue

    data.append(go.Line(x=x,
                        y=rates[col].values,
                        error_y=dict(type='data',
                                     array=rates[f'd{col}'],
                                     visible=True,
                                     width=0),
                        name=col))

data.append(go.Line(x=x,
                    y=prod_rate.values,
                    name='Liquifier Production (sum)',
                    error_y=dict(type='data',
                                 array=dprod_rate.values,
                                 visible=True,
                                 width=0),
                    line=dict(width=5, color='black'))
                )
fig = go.Figure(data)

fig.update_layout(
    title=f'Rate of Change in Levels over {window_size} min intervals<br><sup>Average production rate of liquifier: {prod_rate.mean():.2f} +/- {prod_rate.std():.2f} L/h</sup>',
#    xaxis_title=f'Last updated {datetime.datetime.now()}',
    yaxis_title='Change in Level or Flow (Liquid L/h)',
    font=dict(
        family="Arial",
        size=18,
        color="Black"
    ),
    plot_bgcolor='rgba(0,0,0,0)',
    width=1200*0.75,
    height=800*0.75,
)

fig.update_xaxes(showline=True, linewidth=2, linecolor='black', gridcolor='Gray', zerolinecolor='Gray')
fig.update_yaxes(showline=True, linewidth=2, linecolor='black', gridcolor='Gray', zerolinecolor='Gray')

fig.write_html('/home/ucn/online/ucn-web-control/liquid_prod_rate_fig.html')

