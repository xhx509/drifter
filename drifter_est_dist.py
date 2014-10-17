# -*- coding: utf-8 -*-
"""
Created on Fri May 23 14:29:29 2014

@author: hxu

Created on Thu Apr 10 09:18:26 2014
this program works for comparing real drift track and a model drift track.
it will show a graph of distance between real and model drifters at the end.
Before running this program, please modify data below
input values: drifter number,date,days, filename of real drifter track
output values: real drifter lats,lons.   estimated drifter lats lons ,  distance between real and model drifters
"""
###############################
driftnumber='139420692'  #num of drifter
date='20131023'   #date
days=9 #how many days do you want to plot
filename='http://www.nefsc.noaa.gov/drifter/drift_tcs_2013_1.dat'
#############################
#import datetime
import sys
import numpy as np
pydir1='/home/hxu/epd73/epd-7.3-2-rh5-x86_64/lib/python2.7/site-packages'
sys.path.append(pydir1)

#import datetime as dt
import matplotlib.mlab as ml
import matplotlib.pyplot as plt
sys.path.append('/net/home3/ocn/jmanning/py/mygit/modules/')
#from basemap import basemap_region
from matplotlib.dates import date2num, num2date
from pydap.client import open_url
import netCDF4
from pandas import *
#import collections
from datetime import datetime

def get_dataset(url):
    try:
        dataset = open_url(url)
    except:
        print 'Sorry, ' + url + 'is not available' 
        sys.exit(0)
    return dataset
def getdrift(id):
    """
    uses pydap to get remotely stored drifter data given an id number
    """
    url = 'http://gisweb.wh.whoi.edu:8080/dods/whoi/drift_data'
    
    dataset = get_dataset(url) 
     
    try:
        lat = list(dataset.drift_data[dataset.drift_data.ID == id].LAT_DD)
    except:
        print 'Sorry, ' + id + ' is not available'
        sys.exit(0)
        
    lon = list(dataset.drift_data[dataset.drift_data.ID == id].LON_DD)
    time0 = list(dataset.drift_data[dataset.drift_data.ID == id].TIME_GMT)
    yearday = list(dataset.drift_data[dataset.drift_data.ID == id].YRDAY0_GMT)
    #dep = list(dataset.drift_data[dataset.drift_data.ID == id].DEPTH_I)
    numtime=[]
    for i in range(len(time0)):
        numtime.append(date2num(datetime.strptime(time0[i][:4], '%Y'))+yearday[i])
    keydict = dict(zip(lat, numtime))
    lat.sort(key=keydict.get)
    keydict = dict(zip(lon, numtime))
    lon.sort(key=keydict.get)
    drifter_data={}
    drifter_data['lat']=lat; drifter_data['lon']=lon; drifter_data['time']=time0
    return drifter_data
    
def getdrift_raw(filename,driftnumber,days,datetime_wanted):
    
  # range_time is a number,unit by one day.  datetime_wanted format is num
  d=np.genfromtxt(filename)
  lat1=d[:,8]
  lon1=d[:,7]
  idd=d[:,0]
  year=[]
  for n in range(len(idd)):
      year.append(str(idd[n])[0:2])
  h=d[:,4]
  day=d[:,3]
  month=d[:,2]
  time1=[]
  for i in range(len(idd)):
      time1.append(date2num(datetime.strptime(str(int(h[i]))+' '+str(int(day[i]))+' '+str(int(month[i]))+' '+str(int(year[i])), "%H %d %m %y")))


  idg1=list(ml.find(idd==int(driftnumber)))
  idg2=list(ml.find(np.array(time1)<=datetime_wanted+days))
 
  "'0.25' means the usual Interval, It can be changed base on different drift data "
  idg3=list(ml.find(np.array(time1)>=datetime_wanted-0.1))
  idg23=list(set(idg2).intersection(set(idg3)))
  # find which data we need
  idg=list(set(idg23).intersection(set(idg1)))
  print idg
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
def getnum_driftermodel(date): 
    # there are vary number lists in different time, this fuction uses for finding how many lists are in a time
    url='http://tds.marine.rutgers.edu:8080/thredds/dodsC/floats/espresso_flt_'+date+'.nc'
    database= netCDF4.Dataset(url)
    num=list(np.shape(database.variables['lat']))[1]
    return num

from math import radians, cos, sin, asin, sqrt
def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    km = 6367 * c
    return km


#date=datetime.strptime(date, '%Y%m%d')
####################################################################

datetime_wanted=date2num(datetime.strptime(date, '%Y%m%d'))
#drifter_data=getdrift(driftnumber)
drifter_data=getdrift_raw(filename,driftnumber,days,datetime_wanted)
print drifter_data['lat']
#plt.plot(np.reshape(drifter_data['lon'],np.size(drifter_data['lon'])),np.reshape(drifter_data['lat'],np.size(drifter_data['lat'])),linewidth=2,color='orange')
for z in range(days):
  num=getnum_driftermodel(date) #how many drifter modles at this date
  
  url='http://tds.marine.rutgers.edu:8080/thredds/dodsC/floats/espresso_flt_'+date+'.nc?ocean_time[0:1:312],lon[0:1:312][0:1:'+str(num-1)+'],lat[0:1:312][0:1:'+str(num-1)+']'
#midtime=2.456352E8
  database= netCDF4.Dataset(url)
  lat=database.variables['lat']
  lon=database.variables['lon']
  ocean_time=database.variables['ocean_time']
  ocean_time=ocean_time[0:].tolist()
  lat=lat[0:].tolist()
  lon=lon[0:].tolist()
  lat_l=[]
  lon_l=[]
  time=[]
  for m in range(num):
    for i in range(len(lat)):
        lat_l.append(lat[i][m])
        lon_l.append(lon[i][m])
        time.append(ocean_time[i])
  time_l=np.split(np.array(time), num)
  lat_l=np.split(np.array(lat_l), num)
  lon_l=np.split(np.array(lon_l), num)
  for n in range(len(time_l)):      #delete 'none' data
    id_bad=ml.find(np.array(lat_l[n])<=0)    
    list_lat=list(lat_l[n])
    list_lon=list(lon_l[n])
    list_time=list(time_l[n])
         #print id_bad
    id_bad=list(id_bad)   
    #print len(id_bad)
    if len(id_bad)==len(list_lat):
       continue
    id_bad.reverse()
    for m in id_bad:  
              del list_lat[m]
              del list_lon[m]
              del list_time[m]
            
  for i in range(len(drifter_data['lat'])): 
           if abs(list_lat[0]-drifter_data['lat'][i])<0.1 and abs(list_lon[0]-drifter_data['lon'][i])<0.1:
              for x in range(1,len(list_lat)):
                  if abs(list_lat[0]-list_lat[x])<0.001 and abs(list_lon[0]-list_lon[x])<0.001:
                      break
                  
                  list_lat=list_lat[:x]
                  list_lon=list_lon[:x]
                  list_time=list_time[:x]
                  #print x
                  #print i
                  plt.plot(np.reshape(list_lon,np.size(list_lon)),np.reshape(list_lat,np.size(list_lat)),color='blue')
                  break
  period_str,dist=[],[]
  drifter_data2=getdrift_raw(filename,driftnumber,days,date2num(datetime.strptime(date, '%Y%m%d')))
  for q in range(len(drifter_data2['lat'])):
        for p in range(len(list_time)):
            if abs(drifter_data2['time'][q]-list_time[p]/3600-666371.0)<=0.35:  # list_time add '666762' to become a number date
             
                km=haversine(drifter_data2['lon'][q], drifter_data2['lat'][q], list_lon[p], list_lat[p]) #get distance from real drifter to every est point
                dist.append(km)
                period_str.append(num2date(list_time[p]/3600+666371))  # get right num  datetime, the number may not good, you can change it

                df_d=DataFrame(np.array(dist),index=period_str,columns=['dist'])
                df_d.plot(title=driftnumber)
                plt.gcf().autofmt_xdate()
                plt.xlabel('time')
                plt.ylabel('distance (km)')
                  
           
    #plt.annotate('start',xy=(list_lon[0],list_lat[0]),xytext=(list_lon[0]+(max(list_lon)-min(list_lon))/10,list_lat[0]+(max(list_lat)-min(list_lat))/10),color='red',arrowprops=dict(facecolor='white',frac=0.3, shrink=0.05))
    #plt.annotate('end',xy=(list_lon[-1],list_lat[-1]),xytext=(list_lon[-1]+(max(list_lon)-min(list_lon))/10,list_lat[-1]-(max(list_lat)-min(list_lat))/5),color='red',arrowprops=dict(facecolor='white',frac=0.3, shrink=0.05))
  date=(num2date(date2num(datetime.strptime(date, '%Y%m%d'))+1)).strftime('%Y%m%d')
  
#[lat1, lon1, dep, time0, yearday]=getdrift(driftnumber)
#lat=collections.Counter(lat)
#lon=collections.Counter(lon)



plt.savefig('drift_est_roms_'+driftnumber + '.png') # save file in current directory
plt.show() #show picture

    
      
    
    