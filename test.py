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
from basemap import basemap_region
import datetime as dt
import sys
import os
import pytz, pylab
import numpy as np
import matplotlib.pyplot as plt
from drifter_functions import getobs_drift_byrange,getobs_drift_byidrange,colors,getobs_drift_byid
ops=os.defpath
pydir='../'
sys.path.append(pydir)
#################Input values#############################################

fig = plt.figure()
ax = fig.add_subplot(111)  


plt.plot(-67.8914,41.698,'.',markersize=30,color='black')
basemap_region('ne')    
    

ax.patch.set_facecolor('lightblue')   #set background color

plt.legend( numpoints=1,loc=2)  
#plt.savefig('./'+dt.datetime.now().strftime('%Y-%m-%d %H:%M') + '.png')
 
#datetime_wanted=date2num(num2date(datetime_wanted)+datetime.timedelta( 0,step_size*60*60 ))
plt.show()
