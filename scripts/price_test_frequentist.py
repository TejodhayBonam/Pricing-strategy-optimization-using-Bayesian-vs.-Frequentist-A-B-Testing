#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 19 17:21:21 2017

@author: jeremy
"""

import pandas as pd
from scipy.stats import beta, norm, uniform
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind
###issue changing timestamp to datetime


user_table=pd.read_csv('../user_table.csv')
test = pd.read_csv('../test_results.csv')

#a=test.duplicated('user_id')
a=test.drop_duplicates('user_id')
date=[]
for index,row in test.iterrows():
    tmp=row['timestamp'].split(' ')[0]
    date.append(tmp)

test['date']=date

test['date']=pd.to_datetime(test.date,errors='raise')

test=test.sort_values('date')
NaT=test.query('date=="NaT"')

a = test[test['price']==39]
a_count=a[['converted','date']].groupby('date').count()
a_count.columns.values[0]='count_group_a'
a_count=a_count.reset_index()


b = test[test['price']==59]


c=a[a['date']<='2015-3-10']

day=0

mean_a=[]
mean_b=[]
p_values=[]
for index,row in a_count.iterrows():
   day+=1
   print('Day: ',day)
   current_date=row['date']
   tmp_a=a[a['date']<=current_date]
   tmp_b=b[b['date']<=current_date]
   #Welch's t-test
   t_stat,p_value=ttest_ind(tmp_a['converted']*39/59,tmp_b['converted'],equal_var=False)
   tmp_a['converted']=tmp_a['converted']*39/59
   mean_a.append(tmp_a['converted'].mean())
   mean_b.append(tmp_b['converted'].mean())
   p_values.append(p_value)
   if p_value<.05:
       break
   
x=list(range(1,len(p_values)+1)) 
fig, (dx) = plt.subplots(1, 1)
dx.plot(x,p_values)
dx.set_title('P value (from Welch\'s t-test) vs Time')
dx.set_ylabel('P value')
dx.set_xlabel('Time in Days')
#plt.axis([0, 92, -.0005, .003])
#dx.set_yscale('log')
dx.plot([1,6],[.05,.05])

fig, (ax) = plt.subplots(1, 1)
ax.plot(x,mean_a)
ax.set_title('Mean vs Time (Price=39)')
ax.set_ylabel('Effective Mean')
ax.set_xlabel('Time in Days')


fig, (bx) = plt.subplots(1, 1)
bx.plot(x,mean_b)
bx.set_title('Mean vs Time (Price=59)')
bx.set_ylabel('Mean')
bx.set_xlabel('Time in Days')


      