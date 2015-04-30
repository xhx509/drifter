# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 12:52:09 2015

@author: hxu
"""
import matplotlib.mlab as ml
import datetime as dt
import basemap_xu
import sys
import glob
from matplotlib.dates import num2date,date2num
import numpy as np
from drifter_functions import hexcolors
pydir='../'
sys.path.append(pydir)


filename='seal.dat'
drifter_num=[23,130400661.0, 134402201.0, 156490031.0, 130400671.0, 120350752.0, 120350753.0, 140360731.0, 130400681.0, 130400682.0, 130260781.0, 130260783.0, 154490031.0, 145350201.0, 120350751.0, 125350721.0, 125350722.0, 125350723.0, 125350724.0, 125350725.0, 142270151.0, 142270152.0, 136230731.0, 130400672.0, 152410671.0, 153340771.0, 153340772.0, 130290791.0, 130290792.0, 140350701.0, 140350702.0, 140350703.0, 140350704.0, 152350705.0, 145380091.0]

colors=hexcolors(len(drifter_num))

FN=glob.glob('*.dat') # get all csv files in 1 folder
mymap = basemap_xu.maps(30, -60, 4)

for filename in FN:
  d=np.genfromtxt(filename)
  lat1=d[:,8]
  lon1=d[:,7]
  idd=d[:,0]

#mymap = basemap_xu.maps(np.mean(lat1), np.mean(lon1), 12)  
  for x in range(len(drifter_num)): 

    idg1=list(ml.find(idd==drifter_num[x]))
  #idg2=list(ml.find(np.array(time1)<=datetime_wanted+interval/ 24))
    "'0.25' means the usual Interval, It can be changed base on different drift data "
  #idg3=list(ml.find(np.array(time1)>=datetime_wanted-0.1))
  #idg23=list(set(idg2).intersection(set(idg3)))
  # find which data we need
    idg=idg1
    if len(idg)==0:
        continue
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
        #mymap.addpoint(lat[i],lon[i],'black')
    #mymap.addradpoint(drifter_data[lat][0],lon[0], 95, "#FF0000","my-location")
    mymap.addradpoint(lat[0],lon[0], 295, "red")
    mymap.addradpoint(lat[-1],lon[-1], 295, "blue")
    mymap.addpath(path,colors[x])#00FF00
    #mymap.coloricon
    #mymap.getcycle
    #mymap.zoom    

  #mymap.setgrids(37.42, 43.43, 0.1, -70.15, -60.14, 0.1)

mymap.draw('./'+dt.datetime.now().strftime('%Y-%m-%d %H:%M') +'.html')


'''
def getdrift_raw_simple(filename,id3):
    
  # range_time is a number,unit by one day.  datetime_wanted format is num
  d=np.genfromtxt(filename)
  lat1=d[:,8]
  lon1=d[:,7]
  idd=d[:,0]
  print set(idd)
  year=[]
  for n in range(len(idd)):
      year.append(str(idd[n])[0:2])
  h=d[:,4]
  day=d[:,3]
  month=d[:,2]
  time1=[]
  for i in range(len(idd)):
      time1.append(date2num(dt.datetime.strptime(str(int(h[i]))+' '+str(int(day[i]))+' '+str(int(month[i]))+' '+str(int(year[i])), "%H %d %m %y")))


  idg=list(ml.find(idd==id3))
  print 'the length of drifter data is  '+str(len(idg)),str(len(set(idg)))+'   . if same, no duplicate'
  lat,lon,time=[],[],[]
  
  for x in range(len(idg)):
      lat.append(round(lat1[idg[x]],4))
      lon.append(round(lon1[idg[x]],4))
      time.append(round(time1[idg[x]],4))
  drifter_data={}
  drifter_data['lat']=lat; drifter_data['lon']=lon; drifter_data['time']=time
  # time is num
  return drifter_data
drifter_data=  getdrift_raw_simple(filename,id)
'''