#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 21:45:05 2017

@author: jeremy
"""
import plotly
import plotly.plotly as py
import pandas as pd
plotly.tools.set_credentials_file(username='Jeremy123W', api_key='9tTjUoqWGmintnbZp99d')


user_table=pd.read_csv('../user_table.csv')
test = pd.read_csv('../test_results.csv')


test=test.merge(user_table,how='left',on='user_id')


non_convert=test[test['converted']==0]
convert=test[test['converted']==1]

nonconverted_per_city=non_convert[['city','converted']].groupby(['city']).count()
nonconverted_per_city.columns.values[0]='non_convert_count_per_city'
nonconverted_per_city=nonconverted_per_city.reset_index()


a=test[['city','lat','long']]
a=a.drop_duplicates()
a=a[(a['lat']!=27.76)&(a['long']!=30.31)]  #remove users in saint petersburg russia

df=nonconverted_per_city.merge(a[['city','lat','long']],how='left',on='city')


df=df.sort_values('non_convert_count_per_city',ascending=False)
df=df.dropna()
df=df.reset_index()


df['text'] = df['city'] + '<br>Missed Conversion Count per City ' + (df['non_convert_count_per_city']).astype(str)
limits = [(0,1),(1,5),(5,13),(13,35),(35,132),(132,923)]
colors = ["rgb(0,116,217)","rgb(255,65,54)","rgb(133,20,75)","rgb(255,133,27)","rgb(85,107,47)","lightgrey"]
cities = []
scale = 10
limit_count=[(25305,8000),(7999,4000),(3999,2000),(1999,1000),(999,500),(499,1)]

for i in range(len(limits)):
    lim = limits[i]
    lim_count=limit_count[i]
    df_sub = df[lim[0]:lim[1]]
    city = dict(
        type = 'scattergeo',
        locationmode = 'USA-states',
        lon = df_sub['long'],
        lat = df_sub['lat'],
        text = df_sub['text'],
        marker = dict(
            size = df_sub['non_convert_count_per_city']/scale,
            color = colors[i],
            line = dict(width=0.5, color='rgb(40,40,40)'),
            sizemode = 'area'
        ),
        name = str('{0:<5} - {1:<5} Missed Conversion Count'.format(lim_count[0],lim_count[1]) ) )
        
    cities.append(city)

layout = dict(
        title = 'Missed Conversion Count by US City<br>(Click legend to toggle traces)',
        showlegend = True,
        geo = dict(
            scope='usa',
            projection=dict( type='albers usa' ),
            showland = True,
            landcolor = 'rgb(217, 217, 217)',
            subunitwidth=1,
            countrywidth=1,
            subunitcolor="rgb(255, 255, 255)",
            countrycolor="rgb(255, 255, 255)"
        ),
    )

fig = dict( data=cities, layout=layout )
py.iplot( fig, validate=False, filename='bubble-map-_non_conver_count' )

