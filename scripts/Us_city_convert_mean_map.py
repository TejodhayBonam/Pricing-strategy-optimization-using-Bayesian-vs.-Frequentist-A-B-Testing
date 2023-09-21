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
converted_mean_per_city=test[['city','converted']].groupby(['city']).mean()
converted_mean_per_city.columns.values[0]='converted_mean_per_city'
converted_mean_per_city=converted_mean_per_city.reset_index()

a=test[['city','lat','long']]
a=a[(a['lat']!=27.76)&(a['long']!=30.31)]  #remove users in saint petersburg russia
a=a.drop_duplicates('city')

df=converted_mean_per_city.merge(a[['city','lat','long']],how='left',on='city')
#test=test.merge(nonconverted_per_city,how='left',on='city')
#test=test.merge(converted_mean_per_city,how='left',on='city')

df=df.sort_values('converted_mean_per_city',ascending=False)
df=df.dropna()
df=df.reset_index()
#df = pd.read_csv('2014_us_cities.csv')
#df.head()

df['text'] = df['city'] + '<br>Converted Mean per City ' + (df['converted_mean_per_city']).astype(str)
limits = [(0,3),(3,9),(9,34),(34,132),(40,692),(692,923)] #40
colors = ["rgb(0,116,217)","rgb(255,65,54)","rgb(133,20,75)","rgb(255,133,27)","rgb(85,107,47)","lightgrey"]
limit_count=[(.2,.14),(.12,.08),(.079,.05),(.049,.03),(.029,.01),(.009,0)]
cities = []
scale = 5000

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
            size = df_sub['converted_mean_per_city']*scale,
            color = colors[i],
            line = dict(width=0.5, color='rgb(40,40,40)'),
            sizemode = 'area'
        ),
        name = '{0:<2} - {1:<2} Converted Mean'.format(lim_count[0],lim_count[1]) )
    cities.append(city)

layout = dict(
        title = 'Converted Mean by US City <br>(Click legend to toggle traces)',
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
py.iplot( fig, validate=False, filename='bubble-map-_converted_mean_count' )
