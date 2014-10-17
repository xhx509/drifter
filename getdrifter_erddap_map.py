# -*- coding: utf-8 -*-
"""
Created on Thu Aug 28 14:06:57 2014

@author: hxu
"""
######################
#use for plotting a track of drifter,  data extracted from erddap
#the drifter would be plotted on google map
#Input values:datetime_wanted,filename,model_option,num,interval_dtime,interval,step_size
#output values:gbox,id
#function uses: getobs_drift_byidrange,getobs_drift_byrange
######################

import pygmaps
import sys
import numpy as np
pydir='../'
sys.path.append(pydir)
import datetime as dt
import pytz
from hx import getobs_drift_byrange,colors,getobs_drift_byidrange,getobs_drift_byid

###############################################
#################Input values#############################################
input_time=[dt.datetime(2013,1,1,0,0,0,0,pytz.UTC),dt.datetime(2013,7,1,0,0,0,0,pytz.UTC)] # start time and end time
gbox=[-70.0,-72.0,42.0,40.0] #  maxlon, minlon,maxlat,minlat
id=[134410701] # id list, if you are not clear dedicated id, let id=[]
#'125450842''125450841'
#↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑Input values↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑#
if id==[]:
    
    time,ids,lats,lons=getobs_drift_byrange(gbox,input_time)
    id=list(set(ids))
    rgbcolors=colors(len(id))
    mymap = pygmaps.maps(np.mean(lats), np.mean(lons), 12)
    for k in range(len(id)):
        time,ids,lat,lon=getobs_drift_byidrange(id[k],gbox,input_time)
        
        path=[]
        for i in range(len(lat)):
          path.append((lat[i],lon[i]))
          mymap.addpoint(lat[i],lon[i],'black')
  #mymap.addradpoint(drifter_data[lat][0],drifter_data[1][0], 95, "#FF0000","my-location")
        mymap.addradpoint(lat[0],lon[0], 295, "red")
        mymap.addradpoint(lat[-1],lon[-1], 295, "blue")
        mymap.addpath(path,rgbcolors[k])#00FF00
  #mymap.coloricon
  #mymap.getcycle
  #mymap.zoom    

  #mymap.setgrids(37.42, 43.43, 0.1, -70.15, -60.14, 0.1)
else:
    rgbcolors=colors(len(id))
    for m in range(len(id)):
        time,ids,lat,lon=getobs_drift_byid(id[m],input_time)
        mymap = pygmaps.maps(np.mean(lat), np.mean(lon), 12)
        path=[]
        for i in range(len(lat)):
          path.append((lat[i],lon[i]))
          #mymap.addpoint(lat[i],lon[i],'black')
  #mymap.addradpoint(drifter_data[lat][0],drifter_data[1][0], 95, "#FF0000","my-location")
        mymap.addradpoint(lat[0],lon[0], 295, "red")
        mymap.addradpoint(lat[-1],lon[-1], 295, "blue")
        mymap.addpath(path,[50, 50, 0.0])#00FF00
        
mymap.draw('./mymap.html')
    
