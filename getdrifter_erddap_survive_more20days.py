# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 16:05:44 2015

@author: hxu

"""
"""
Please run 'driftersuvive_main.py'

it used for getting drifter survive information(not include drifter less than 20 days or ashore) from erddap based on id_list and time_period ()
Before running this program, ask Huanxin to get drifter id from 'nova' service
After running this program, it could plot a graph of drifter survive. And you could save that by yourself
input values: time period,ids
function uses:getobs_drift_byid, getobs_drift_byrange, haversine,get_coastline_coordinate
output : a plot with average days and total drifters , saving figure name is like 1980-2015-09.png
"""
import time
import datetime as dt
import sys
import os
import matplotlib.pyplot as plt
import pytz
from pandas import *
#import pandas.tools.rplot as rplot
from matplotlib.dates import date2num
from drifter_functions import getobs_drift_byrange,getobs_drift_byid,get_coastline_coordinate,haversine
ops=os.defpath
pydir='../'
sys.path.append(pydir)
#################Input values#############################################

#↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑Input values↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑#
drifter_name=['Rachel','Eddie','Cassie','Irina']
drifter_type=['plastic', '2x4wood', 'bamboo', 'aluminum']  # names of 4 subplots , they can be changed
fig, axes = plt.subplots(nrows=2, ncols=2,figsize=(20,12))
axes = axes.ravel()  #get axes
for y in range(len(ids)):
    
    id=[int(a) for a in ids[y]]  # convert to ints

    if id==[]:
        time,ids_un,lat,lon=getobs_drift_byrange(gbox,input_time)  #get  and organize data

    else:
        every_time_total,id_s=[],[]
        totalday=0;total_drifter=0
        region='wv'
        lat_data, lon_data=get_coastline_coordinate(region)  # gets coastline coordinate
        for q in range(len(id)):
            print id[q]
            time,id_un,lat,lon=getobs_drift_byid(id[q],input_time)  #get  and organize data
            distance=0
            for z in range(len(lat_data)):
                if haversine(lon_data[z], lat_data[z], lon[-1], lat[-1])< 0.5: #1.0 represent  1 kilometer   , get rid of landed drifter
                    #print haversine(lon_data[z], lat_data[z], lon[-1], lat[-1])
                    distance=1
                    break
            if distance==0:
                every_time_total.append(date2num(time[-1])-date2num(time[0]))
                totalday=totalday+date2num(time[-1])-date2num(time[0])  
                total_drifter+=1 # get number of total ploted drifters
        drifter_n,index_day=[],[];  
        for i in range(1,15): #set y columns to 30 columns
             drifter_n.append(len([x for x in every_time_total if (20*i+20)>x >= (20*i)]))
             index_day.append(str(20*i)+'-'+str(20*i+20))  # for setting y label
        shortterm_drifter_n= len([w for w in every_time_total if (20)>w >= (0)])
        totalday20=sum([w for w in every_time_total if (20)>w >= (0)])
        df=DataFrame(np.array(drifter_n),index=index_day,columns=[drifter_type[y]])  # generate a dataframe
        ax=axes[y]
        #df.plot(ax=axes[y],title=drifter_name[y],color='r')
        #df.plot(ax=axes[y],kind='bar',title=drifter_name[y],ylim=[0,50])  #plot graph
        #plt.setp( ax,xticks=np.arange(len(temp_r_std)),xticklabels=temp_r_std )        
        df.plot(ax=axes[y],kind='bar',ylim=[0,35])
        '''
        ax.text(0.5, 0.8, 'average '+str(round((totalday-totalday20)/(sum(drifter_n)),1))+' days'+'\nTotal drifters #'+str(total_drifter-shortterm_drifter_n)+'\nnot including '+str(len(id)-total_drifter)+' drifters ashore\n or '+str(shortterm_drifter_n)+' drifters surviving less than 20 days',
            verticalalignment='top', horizontalalignment='center',
            transform=ax.transAxes,
            color='green', fontsize=25)
        '''       
        ax.text(0.5, 0.92, 'average '+str(round((totalday-totalday20)/(sum(drifter_n)),1))+' days'+'\nTotal drifters #'+str(total_drifter-shortterm_drifter_n)+'\n',
            verticalalignment='top', horizontalalignment='center',
            transform=ax.transAxes,
            color='green', fontsize=25)
        ax.text(0.5, 0.8, '\n\nnot including '+str(len(id)-total_drifter)+' drifters ashore\n or '+str(shortterm_drifter_n)+' drifters surviving less than 20 days',
            verticalalignment='top', horizontalalignment='center',
            transform=ax.transAxes,
            color='green', fontsize=16)
        ax.set_title(drifter_name[y], fontsize=26)    
        ax.set_xlabel('survival period (days)',fontsize=25)   # set label
        ax.set_ylim([0,35])
        if y%2==0:
            ax.set_ylabel('# drifter',fontsize=25)
        if y%2==1:
            plt.setp(ax.get_yticklabels(), visible=False)
         #   ax.set_ylabel('',fontsize=25)
        #ax.add(rplot.TrellisGrid(['sex', 'smoker']))
        plt.gcf().autofmt_xdate()
        #plt.savefig('EDDIE.png')
#plt.setp(ax.get_yticklabels(), visible=False)
#plt.tight_layout()  
#setp(ax.get_yticklabels(), visible=False) 
#plt.title('drifters survive from 1980-'+input_time[1].strftime("%Y"))
mng = plt.get_current_fig_manager()
mng.window.showMaximized()
plt.savefig('1980-'+input_time[1].strftime("%Y-%m")+'.png')
plt.show()
