# -*- coding: utf-8 -*-
"""
Created on Wed Aug 27 10:14:02 2014

@author: hxu
this progress extracts drifter data(coordinates) based on time range, geographic range or drifter id, then plot them.
The ouput file will be in same folder as this program. 
input values: time period,gbox(maxlon, minlon,maxlat,minlat),or time period and id
function uses: getobs_drift_byrange,getobs_drift_byidrange,colors,getobs_drift_byid
output : a plot file to show drifter track.

"""

import datetime as dt
import sys
import os
import pytz, pylab
import numpy as np
import matplotlib.pyplot as plt
from hx import getobs_drift_byrange,colors,getobs_drift_byid,point_in_poly
ops=os.defpath
pydir='../'
sys.path.append(pydir)
#################Input values#############################################
input_time=[dt.datetime(2012,1,1,0,0,0,0,pytz.UTC),dt.datetime(2013,7,1,0,0,0,0,pytz.UTC)] # start time and end time
gbox=[-70.035594,-70.597883,42.766619,42.093197] #  maxlon, minlon,maxlat,minlat
id=[] # id list, if you are not clear dedicated id, let id=[]
#'125450842''125450841'
#↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑Input values↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑#

fig = plt.figure()
ax = fig.add_subplot(111)  
polygon=[(gbox[0],gbox[2]),(gbox[0],gbox[3]),(gbox[1],gbox[3]),(gbox[1],gbox[2])]
if id==[]:
    
    time,ids,lats,lons=getobs_drift_byrange(gbox,input_time)
    id=list(set(ids))
    rgbcolors=colors(len(id))
    for k in range(len(id)):
        time,ids,lat,lon=getobs_drift_byid(id[k],input_time)
        for z in range(len(lat)):
            inside=point_in_poly(lon[z],lat[z],polygon)
            if inside == True:
              break

        lat=lat[z:]
        lon=lon[z:]

        plt.plot(lon[0],lat[0],'.',markersize=30,color=rgbcolors[k+1],label=str(id[k]))
        plt.plot(np.reshape(lon,np.size(lon)),np.reshape(lat,np.size(lat)),color=rgbcolors[k+1])
else:
    lats,lons=[],[]
    rgbcolors=colors(len(id))
    for m in range(len(id)):
        time,ids,lat,lon=getobs_drift_byid(id[m],input_time)
        for z in range(len(lat)):
            inside=point_in_poly(lon[z],lat[z],polygon)
            if inside == True:
              break

        lat=lat[z:]
        lon=lon[z:]
        plt.plot(lon[0],lat[0],'.',markersize=30,color=rgbcolors[m+1],label=str(id[m]))
        plt.plot(np.reshape(lon,np.size(lon)),np.reshape(lat,np.size(lat)),color=rgbcolors[m+1])
        for n in range(len(lat)):  
            lats.append(lat[n])
            lons.append(lon[n])

    
plt.plot([gbox[0],gbox[0],gbox[1],gbox[1],gbox[0]],[gbox[2],gbox[3],gbox[3],gbox[2],gbox[2]],color='black')    
    
plt.title(str(time[0].strftime("%d-%b-%Y %H"))+'h') 
    
#pylab.ylim([min(lats)-(max(lats)-min(lats))/6.0,max(lats)+(max(lats)-min(lats))/6.0])
#pylab.xlim([min(lons)-(max(lons)-min(lons))/6.0,max(lons)+(max(lons)-min(lons))/6.0])

ax.patch.set_facecolor('lightblue')   #set background color

plt.legend( numpoints=1,loc=2)  
plt.savefig('./'+str(time[0].strftime("%d-%b-%Y %H"))+'h' + '.png')
 
#datetime_wanted=date2num(num2date(datetime_wanted)+datetime.timedelta( 0,step_size*60*60 ))
plt.show()
