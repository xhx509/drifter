# -*- coding: utf-8 -*-
"""
Created on Wed Aug 27 10:14:02 2014

@author: hxu
this progress extracts drifter data(coordinates) based on time range, geographic range or drifter id, then plot them.
it only plot the sourse drifter which is before coming to the geographic range.
The ouput html file will be in same folder as this program. 
input values: time period,gbox(maxlon, minlon,maxlat,minlat),or time period and id
function uses: getobs_drift_byrange,getobs_drift_byidrange,colors,getobs_drift_byid,point_in_poly
output : a plot html file to show drifter track on google map.

"""
import basemap_xu
import datetime as dt
import sys
import os
import pytz
import numpy as np
from drifter_functions import getobs_drift_byrange,getobs_drift_byid,point_in_poly,hexcolors
ops=os.defpath
pydir='../'
sys.path.append(pydir)
#################Input values#############################################
input_time=[dt.datetime(1980,1,1,0,0,0,0,pytz.UTC),dt.datetime(2014,10,15,0,0,0,0,pytz.UTC)] # start time and end time
gbox=[-70.035594,-70.597883,42.766619,42.093197] #  maxlon, minlon,maxlat,minlat
id=[] # id list, if you are not clear dedicated id, let id=[]
#'125450842''125450841'
#↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑Input values↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑#

polygon=[(gbox[0],gbox[2]),(gbox[0],gbox[3]),(gbox[1],gbox[3]),(gbox[1],gbox[2])] #set polygon
if id==[]:    
    time,ids,lats,lons=getobs_drift_byrange(gbox,input_time)
    mymap = basemap_xu.maps(np.mean(lats), np.mean(lons), 12)  #set center point of the map
    id=list(set(ids))
    colors=hexcolors(len(id))  #get hex colors,like '00FF00'
    for k in range(len(id)):
        time,ids,lat,lon=getobs_drift_byid(id[k],input_time)  # get data by id
        for z in range(len(lat)):  # make plotting drifter start in gbox
            inside=point_in_poly(lon[z],lat[z],polygon) 
            if inside == True:
              break
        if z>1: 
          lat=lat[0:z-1]   #get rid of drifters which start from the polygon
          lon=lon[0:z-1]
          time=time[0:z-1]
          path=[] #set path, point 
          for i in range(len(lat)):
            path.append((lat[i],lon[i]))
            #mymap.addpoint(lat[i],lon[i],colors[k])
          title='id:'+str(id[k])+'  time on this point:'+time[0].strftime('%d-%m-%Y %H:%M')
          #title='id:'+str(id[k])+'\n starttime'+time[0].strftime('%d-%m-%Y %H:%M') 
          mymap.addpoint(lat[0],lon[0], colors[k],title) #plot them
          mymap.addpath(path,colors[k])
else:
    colors=hexcolors(len(id))#get hex colors,like '00FF00'
    for m in range(len(id)):
        time,ids,lat,lon=getobs_drift_byid(id[m],input_time) # get data by id
        for z in range(len(lat)):  # make plotting drifter start in gbox
            inside=point_in_poly(lon[z],lat[z],polygon)
            if inside == True:
              break
        lat=lat[z:]
        lon=lon[z:]
        
        path=[] #set path, point to plot
        for i in range(len(lat)):
          path.append((lat[i],lon[i]))
          mymap.addpoint(lat[i],lon[i],'black')
        mymap.addradpoint(lat[0],lon[0], 295, "red")
        mymap.addradpoint(lat[-1],lon[-1], 295, "blue")
        mymap.addpath(path,colors[k])#00FF00
    
ranges=[(gbox[2],gbox[0]),(gbox[3],gbox[0]),(gbox[3],gbox[1]),(gbox[2],gbox[1]),(gbox[2],gbox[0])] #plot range you gave
mymap.addpath(ranges,'red')#00FF00    
mymap.draw('./sink_before'+dt.datetime.now().strftime('%Y-%m-%d %H:%M')+'.html')