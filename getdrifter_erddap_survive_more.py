# -*- coding: utf-8 -*-
"""
Created on Thu Nov  6 10:03:59 2014

@author: hxu
"""
"""
Please run 'driftersuvive_main.py'


it used for getting drifter survive information from erddap based on id_list and time_period ()
Before running this program, ask Huanxin to get drifter id from 'nova' service
After running this program, it could plot a graph of drifter survive. And you could save that by yourself
input values: time period,ids
function uses:getobs_drift_byid, getobs_drift_byrange, haversine,get_coastline_coordinate
output : a plot with average days and total drifters 
"""
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

drifter_name=['Rachel','Eddie','Cassie','Irina']  # names of 4 subplots , they can be changed
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
        drifter_n,index_day=[],[]    
        for i in range(15): #set y columns to 30 columns
             drifter_n.append(len([x for x in every_time_total if (20*i+20)>x >= (20*i)]))
             index_day.append(str(20*i)+'-'+str(20*i+20))  # for setting y label
         
        df=DataFrame(np.array(drifter_n),index=index_day,columns=[drifter_name[y]])  # generate a dataframe
        ax=axes[y]
        #df.plot(ax=axes[y],title=drifter_name[y],color='r')
        df.plot(ax=axes[y],kind='bar',title=drifter_name[y],ylim=[0,40])  #plot graph
     
        ax.text(0.5, 0.8, 'average '+str(round(totalday/(q+1),1))+' days'+'\nTotal drifters #'+str(total_drifter)+'\nnot including '+str(len(id)-total_drifter)+' drifters ashore',
            verticalalignment='top', horizontalalignment='center',
            transform=ax.transAxes,
            color='green', fontsize=25)
           
        ax.set_xlabel('days_period',fontsize=25)   # set label
        if y%2==0:
            ax.set_ylabel('# drifter',fontsize=25)
        if y%2==1:
            plt.setp(ax.get_yticklabels(), visible=False)
        #ax.add(rplot.TrellisGrid(['sex', 'smoker']))
        plt.gcf().autofmt_xdate()
        #plt.savefig('EDDIE.png')
#plt.tight_layout()   
plt.show()
plt.savefig('drift_survive_all.png')