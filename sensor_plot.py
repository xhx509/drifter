# -*- coding: utf-8 -*-
"""
Created on Tue Dec 16 09:52:58 2014

@author: hxu
"""
from dateutil.parser import parse
import pytz
import numpy as np
import datetime
import pandas as pd
from pandas import *
import numpy as np
import matplotlib.dates as md
import matplotlib.pyplot as plt
from drifter_functions import colors
f_ori='minilog4.csv'
f_cur='2014-12-18 10:45:45.csv'
#cur_id=24576
#input_time=[dt.datetime(2014,12,15,15,0,0,0,pytz.UTC),dt.datetime(2014,12,16,10,0,0,0,pytz.UTC)]

df1=pd.read_csv(f_cur,parse_dates={'time':[1]},date_parser=parse,names=np.array(['driftid','tme','temp_cur']))

#df2=pd.read_csv(f_ori)
ids=[df1['driftid'][0]]
for i in range(len(df1['driftid'])-1):
    if df1['driftid'][i+1]<>df1['driftid'][i]:
        ids.append(df1['driftid'][i+1])
rgbcolor=colors(len(ids))
variables=['date','tim','temp']
skipr=8
dt=read_csv(f_ori,sep=',',skiprows=skipr,parse_dates={'time':[0,1]},date_parser=parse,names=variables)
time_ori=dt['time'].tolist()
import datetime
time_ori=[(datetime.datetime.strptime(str(q),'%Y-%m-%d %H:%M:%S')-datetime.timedelta(hours=1)) for q in time_ori]
#datetime.datetime.fromtimestamp(). strptime('%Y-%m-%d %H:%M:%S')
temp_ori=dt['temp'].tolist()

fig=plt.figure()
ax=fig.add_subplot(111)
num=0
f = open('./emolt'+datetime.datetime.now().strftime('%Y-%m-%d %H:%M') + '.xls', 'w')  # create file and name it

#f.writelines('site'+'         '+'lat         '+' lon        '+' depth(m)'+'    '+'      time'+'              '+'temp(C)'+'\n')
ax.plot(time_ori,temp_ori,label='minilog',linewidth=3, color='r')
for m in range(len(ids)):
    dfm=df1[df1['driftid'] == ids[m]]
    for n in range(len(dfm)):
        if str(dfm['time'].iloc[n])[0:13]=='2014-12-17 11':
            idx=n          
            continue
    for x in range(len(dfm)):
        if str(dfm['time'].iloc[x])[0:13]=='2014-12-18 09':
            idx2=x          
            continue    
    df2=dfm.iloc[idx:idx2]

    b_te,m_te=[],[]
    for y in range(len(df2)):
        for z in range(len(time_ori)):
            if time_ori[z].strftime('%Y-%m-%d %H:%M')==str(df2['time'].iloc[y])[0:16]:
                
                b_te.append(df2['temp_cur'].iloc[y])
                m_te.append(temp_ori[z])
    mean_mis=np.mean(b_te)-np.mean(m_te)
    RMS=np.sqrt(sum([(b_te[z]-m_te[z])**2 for z in range(len(b_te))])/y)
    print  ids[m], mean_mis , RMS ,y    
    f.writelines(str(ids[m])+','+ str(mean_mis)+','+ str(round(RMS,2))+ ','+str(y)+'\n' )      
    temp_cur=df2['temp_cur'].tolist()
    time_cur=df2['time'].tolist()

   
    #df1.plot(x='time',y='temp_cur')
    ax.plot(time_cur,temp_cur,label=ids[m],linewidth=2, color=rgbcolor[m])
f.close()
ax.set_ylabel('Temperature(C)',fontsize=18)
#ax.set_xlabel('Time Period',fontsize=18)
xfmt = md.DateFormatter('%Y-%m-%d %H:%M:%S')
ax.xaxis.set_major_formatter(xfmt)
ax.legend()
plt.gcf().autofmt_xdate()
#df1.plot(x='time',y='temp_cur')
plt.show()
plt.savefig('test'+'.png')
'''
ori=[19.35,
,9.59
,13.9
,16.8
,18.68
,19.88
,20.63
,21.05
,21.28
,21.37
,21.41
,21.43
,21.42
,21.41
,21.4
,21.38
,21.39
,21.38
,21.43
]

df1['temp_ori']=ori
df1=df1.set_index('time')

df1.plot(x_compat=True)
plt.gcf().autofmt_xdate()
plt.show()
dt=read_csv(f_ori,sep=',',skiprows=skipr,parse_dates={'datet':[0,1]},index_col='datet',date_parser=parse,names=variables)
'''