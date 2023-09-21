#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 19 17:21:21 2017

@author: jeremy
"""

import pandas as pd
import bayesian_ab
from scipy.stats import beta, norm, uniform
import matplotlib.pyplot as plt
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
a_sum=a[['converted','date']].groupby('date').sum()
a_sum.columns.values[0]='sum_converted_a'
a_sum=a_sum.reset_index()
a_count=a[['converted','date']].groupby('date').count()
a_count.columns.values[0]='count_group_a'
a_count=a_count.reset_index()

a_join= a_sum.merge(a_count,how='inner',on='date')


b = test[test['price']==59]
b_sum=b[['converted','date']].groupby('date').sum()
b_sum.columns.values[0]='sum_converted_b'
b_sum=b_sum.reset_index()
b_count=b[['converted','date']].groupby('date').count()
b_count.columns.values[0]='count_group_b'
b_count=b_count.reset_index()

b_join= b_sum.merge(b_count,how='inner',on='date')

ab_merge= a_join.merge(b_join,how='inner',on='date')

day=0
#using uninformed priors
prior_params = [ (1, 1), (1,1) ]
#threshold for the error to terminate test
threshold_of_caring = 0.0001
errors=[]
N=[0,0]
s=[0,0]
for index,row in ab_merge.iterrows():
    day+=1
    print('Day: ',day)
    N[0]+=row['count_group_a']
    N[1]+=row['count_group_b']
    s[0]+=(row['sum_converted_a']*39/59)
    s[1]+=row['sum_converted_b']
    error,pdf_arr=bayesian_ab.bayesian_test(N,s,prior_params,threshold_of_caring)
    errors.append(error)
    if error<threshold_of_caring:
        break
    
bayesian_ab.graph(N,s,prior_params,pdf_arr)   
x=list(range(1,len(errors)+1)) 
fig, (dx) = plt.subplots(1, 1)
dx.plot(x,errors)
dx.set_title('Expected Error vs Time')
dx.set_ylabel('Expected Error (horizontal line is threshold of caring)')
dx.set_xlabel('Time in Days')
#plt.axis([0, 92, -.0005, .003])
dx.set_yscale('log')
dx.plot([1,6],[.0001,.0001])
      