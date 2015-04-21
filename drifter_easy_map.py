# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 10:19:48 2015

@author: hxu

This use for plot track of drifter, temporary, from a txt file"
"""
######################
#This uses for plotting a track of drifter, use ctl file "getcodar_ctl.txt"
#the drifter would be plotted on google map
#Input values:datetime_wanted,filename,model_option,num,interval_dtime,interval,step_size
#output values:gbox,id
#function uses:getcodar_ctl_file,getdrift_raw
######################
import datetime as dt
import pygmaps
import sys
import numpy as np
import matplotlib.mlab as ml
pydir='../'
sys.path.append(pydir)
from drifter_functions import getcodar_ctl_file,hexcolors
import basemap_xu
###############################################
filename='./123.txt'

drifter_num=[3534,3546,3578,3586]
#drifter_num=[3534]
colors=hexcolors(len(drifter_num))
  #change format
d=np.genfromtxt(filename)
lat1=d[:,4]
lon1=d[:,3]
idd=d[:,0]
mymap = basemap_xu.maps(np.mean(lat1), np.mean(lon1), 12)  
for x in range(len(drifter_num)): 

  idg1=list(ml.find(idd==drifter_num[x]))
  #idg2=list(ml.find(np.array(time1)<=datetime_wanted+interval/ 24))
  "'0.25' means the usual Interval, It can be changed base on different drift data "
  #idg3=list(ml.find(np.array(time1)>=datetime_wanted-0.1))
  #idg23=list(set(idg2).intersection(set(idg3)))
  # find which data we need
  idg=idg1
  print 'the length of drifter data is  '+str(len(idg)),str(len(set(idg)))+'   . if same, no duplicate'
  lat,lon,time=[],[],[]
  
  for u in range(len(idg)):
      lat.append(round(lat1[idg[u]],4))
      lon.append(round(lon1[idg[u]],4))
      #time.append(round(time1[idg[u]],4)) 
  print len(lat)    

  path=[]
  for i in range(len(lat)):
      path.append((lat[i],lon[i]))
      mymap.addpoint(lat[i],lon[i],'black')
  #mymap.addradpoint(drifter_data[lat][0],lon[0], 95, "#FF0000","my-location")
  mymap.addradpoint(lat[0],lon[0], 295, "red")
  mymap.addradpoint(lat[-1],lon[-1], 295, "blue")
  mymap.addpath(path,colors[x])#00FF00
  #mymap.coloricon
  #mymap.getcycle
  #mymap.zoom    

  #mymap.setgrids(37.42, 43.43, 0.1, -70.15, -60.14, 0.1)

mymap.draw('./'+dt.datetime.now().strftime('%Y-%m-%d %H:%M') +'.html')
