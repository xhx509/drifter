

# -*- coding: utf-8 -*-
"""
Created on Mon Oct 15 15:32:36 2012

@author: huanxin

This use for plot track of drifter, use ctl file "getcodar_ctl.txt"
"""
######################
#This uses for plotting a track of drifter, use ctl file "getcodar_ctl.txt"
#the drifter would be plotted on google map
#Input values:datetime_wanted,filename,model_option,num,interval_dtime,interval,step_size
#output values:gbox,id
#function uses:getcodar_ctl_file,getdrift_raw
######################

import pygmaps
import sys
import numpy as np
pydir='../'
sys.path.append(pydir)
from hx import getcodar_ctl_file,getdrift_raw

###############################################
inputfilename='./getcodar_bydrifter_ctl.txt'


(datetime_wanted,filename,driftnumber,url,model_option,num,interval_dtime,interval,step_size)=getcodar_ctl_file(inputfilename)
id3=int(driftnumber)  #change format
for x in range(num): 
  (drifter_data)=getdrift_raw(filename,id3,interval,datetime_wanted)
  mymap = pygmaps.maps(np.mean(drifter_data[0]), np.mean(drifter_data[1]), 12)
  path=[]
  for i in range(len(drifter_data[0])):
      path.append((drifter_data[0][i],drifter_data[1][i]))
      mymap.addpoint(drifter_data[0][i],drifter_data[1][i],'black')
  #mymap.addradpoint(drifter_data[lat][0],drifter_data[1][0], 95, "#FF0000","my-location")
  mymap.addradpoint(drifter_data[0][0],drifter_data[1][0], 295, "red")
  mymap.addradpoint(drifter_data[0][-1],drifter_data[1][-1], 295, "blue")
  mymap.addpath(path,"green")#00FF00
  #mymap.coloricon
  #mymap.getcycle
  #mymap.zoom    

  #mymap.setgrids(37.42, 43.43, 0.1, -70.15, -60.14, 0.1)

  mymap.draw('./'+str(id3))
