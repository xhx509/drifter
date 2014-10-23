# -*- coding: utf-8 -*-
"""
Created on Wed Oct 10 15:23:37 2012

@author: Huanxin


"""
#this is a functional package working for overlays program
#########################################
import math
import pandas as pd
from dateutil.parser import parse
#import matplotlib
import scipy
import datetime
import numpy
import matplotlib.pyplot as plt
from matplotlib.dates import num2date,date2num
from matplotlib.dates import  DateFormatter
import datetime as dt
import pylab
from pydap.client import open_url
import sys
#pydir='/net/home3/ocn/jmanning/py/huanxin/work'
import numpy as np
import matplotlib.mlab as ml
import time
import pytz
utc = pytz.timezone('UTC')
#sys.path.append(pydir)


def colors(n):
    """Compute a list of distinct colors, each of which is represented as an RGB 3-tuple."""
    """It's useful for less than 100 numbers"""
    if pow(n,float(1)/3)%1==0.0:
        n+=1 
	  #make sure number we get is more than we need.
    rgbcolors=[]
    x=pow(n,float(1)/3)
    a=int(x)
    b=int(x)
    c=int(x)
    if a*b*c<=n:
       a+=1
    if a*b*c<n:
       b+=1
    if a*b*c<n:
       c+=1
    for i in range(a):
       r=0.99/(a)*(i)
       for j in range(b):
          s=0.99/(b)*(j)
          for k in range(c):
             t=0.99/(c)*(k)
             color=r,s,t
             rgbcolors.append(color)
    return rgbcolors



def getcodar_ctl_file(inputfilename):
#open file and read,It is used for get model data
  f=open(inputfilename)  
  dtime=f.readline()
  dtime=dtime[0:dtime.index(']')].strip('[')
  datetime_wanted=date2num(dt.datetime.strptime(dtime,'%Y,%m,%d,%H,%M')) 
  
  filename=f.readline()
  filename=filename[0:filename.index(']')].strip('[').split(',')
  filename=filename[0]
  
  driftnumber=f.readline()
  driftnumber=driftnumber[0:driftnumber.index(']')].strip('[').split(',')
  driftnumber=driftnumber[0] 
  
  num_interval=f.readline()
  num_interval=num_interval[0:num_interval.index(']')].strip('[').split(',')
  print 'number of frames, interval time (hours), step size (hours?) :'+str(num_interval)
  num=int(num_interval[0])
  interval=int(num_interval[1])
  interval_dtime=datetime.timedelta( 0,interval*60*60 )
  step_size=int(num_interval[2])

  
  model_option=f.readline()
  model_option=model_option[0:model_option.index(']')].strip('[')
  model_option=model_option[0]
  
  if model_option=='1':
      url="http://tds.marine.rutgers.edu:8080/thredds/dodsC/cool/codar/totals/macoora6km_fmrc/Macoora_6km_Totals_(FMRC)_best.ncd" 
  if model_option=='2':
      url="http://tds.marine.rutgers.edu:8080/thredds/dodsC/cool/codar/totals/sw06" 
  if model_option=='3':
      url="http://tds.marine.rutgers.edu:8080/thredds/dodsC/cool/codar/totals/macoora6km"          
  if model_option=='4':
      url="http://tds.marine.rutgers.edu:8080/thredds/dodsC/cool/codar/totals/macoora8km"   
  if model_option=='5':
      url="http://tds.marine.rutgers.edu:8080/thredds/dodsC/cool/codar/totals/macoora6km_clone"
  if model_option=='6':
      url="http://tds.marine.rutgers.edu:8080/thredds/dodsC/cool/codar/totals/5Mhz_6km_realtime_fmrc/Maracoos_5MHz_6km_Totals-FMRC_best.ncd"
  return datetime_wanted,filename,driftnumber,url,model_option,num,interval_dtime,interval,step_size

def nearxy(x,y,x0,y0): #find a point in points which we give nera the specified point, calculate dist
    distance=[]
    for i in range(0,np.size(x)):
      for l in range(0,len(y)):
         distance.append(abs(math.sqrt((x[i]-x0)**2+(y[l]-y0)**2)))
    min_dis=min(distance)
    #len_dis=len(distance)
    for p in range(0,len(x)):
      for q in range(0,len(y)):
          if abs(math.sqrt((x[p]-x0)**2+(y[q]-y0)**2))==min_dis:
              index_x=p
              index_y=q
  

    return min(distance),index_x,index_y
  


def getobs_drift_byrange(gbox,input_time):
    """
   Function written by Huanxin and used in "getdrifter_erddap.py"
   get data from url, return id, latitude,longitude, and times
   gbox includes 4 values, maxlon, minlon,maxlat,minlat, like:  [-69.0,-73.0,41.0,40.82]
   input_time can either contain two values: start_time & end_time OR one  value:interval_days
   and they should be timezone aware
   example: input_time=[dt(2012,1,1,0,0,0,0,pytz.UTC),dt(2012,2,1,0,0,0,0,pytz.UTC)]
   """
    lon_max=gbox[0];lon_min=gbox[1];lat_max=gbox[2];lat_min=gbox[3]
    mintime=input_time[0].strftime('%Y-%m-%d'+'T'+'%H:%M:%S'+'Z')  # change time format
    maxtime=input_time[1].strftime('%Y-%m-%d'+'T'+'%H:%M:%S'+'Z')
    # open url to get data
    url='http://comet.nefsc.noaa.gov:8080/erddap/tabledap/drifters.csv?id,time,latitude,longitude&time>='\
    +str(mintime)+'&time<='+str(maxtime)+'&latitude>='\
    +str(lat_min)+'&latitude<='+str(lat_max)+'&longitude>='+str(lon_min)+'&longitude<='+str(lon_max)+'&orderBy("id,time")'
    df=pd.read_csv(url,skiprows=[1])
    for k in range(len(df)):
       df.time[k]=parse(df.time[k])
    return df.time.values,df.id.values,df.latitude.values,df.longitude.values



def getobs_drift_byid(id,input_time):
    """
     Function written  by Huanxin and used by getdrifter_erddap.py
     get data from url, return ids latitude,longitude, times
     input_time can either contain two values: start_time & end_time OR one value:interval_days
     and they should be timezone aware
     example: input_time=[dt(2012,1,1,0,0,0,0,pytz.UTC),dt(2012,2,1,0,0,0,0,pytz.UTC)]
     """
    mintime=input_time[0].strftime('%Y-%m-%d'+'T'+'%H:%M:%S'+'Z')  # change time format
    maxtime=input_time[1].strftime('%Y-%m-%d'+'T'+'%H:%M:%S'+'Z')    
    # open url to get data
    url='http://comet.nefsc.noaa.gov:8080/erddap/tabledap/drifters.csv?id,time,latitude,longitude&time>='\
    +str(mintime)+'&time<='+str(maxtime)+'&id="'+str(id)+'"&orderBy("time")'
    df=pd.read_csv(url,skiprows=[1])
    for k in range(len(df)):
       df.time[k]=parse(df.time[k])
    df=df[df.longitude <=-20]
    return df.time.values,df.id.values,df.latitude.values,df.longitude.values
    
def getobs_drift_byidrange(id,gbox,input_time):
    """
     Function written  by Huanxin and used by getdrifter_erddap.py
     get data from url, return ids latitude,longitude, times
     input_time can either contain two values: start_time & end_time OR one value:interval_days
     and they should be timezone aware
     example: input_time=[dt(2012,1,1,0,0,0,0,pytz.UTC),dt(2012,2,1,0,0,0,0,pytz.UTC)]
     """
    mintime=input_time[0].strftime('%Y-%m-%d'+'T'+'%H:%M:%S'+'Z')  # change time format
    maxtime=input_time[1].strftime('%Y-%m-%d'+'T'+'%H:%M:%S'+'Z')   
    lon_max=gbox[0];lon_min=gbox[1];lat_max=gbox[2];lat_min=gbox[3]
    # open url to get data
    url='http://comet.nefsc.noaa.gov:8080/erddap/tabledap/drifters.csv?id,time,latitude,longitude&time>='\
    +str(mintime)+'&time<='+str(maxtime)+'&latitude>='+str(lat_min)+'&latitude<='+str(lat_max)+'&longitude>='\
    +str(lon_min)+'&longitude<='+str(lon_max)+'&id="'+str(id)+'"&orderBy("id,time")'
    df=pd.read_csv(url,skiprows=[1])
    for k in range(len(df)):
       df.time[k]=parse(df.time[k])

    return df.time.values,df.id.values,df.latitude.values,df.longitude.values

def getdrift_raw(filename,id3,interval,datetime_wanted):
    
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
      time1.append(date2num(datetime.datetime.strptime(str(int(h[i]))+' '+str(int(day[i]))+' '+str(int(month[i]))+' '+str(int(year[i])), "%H %d %m %y")))


  idg1=list(ml.find(idd==id3))
  idg2=list(ml.find(np.array(time1)<=datetime_wanted+interval/24))
  "'0.25' means the usual Interval, It can be changed base on different drift data "
  idg3=list(ml.find(np.array(time1)>=datetime_wanted-0.1))
  idg23=list(set(idg2).intersection(set(idg3)))
  # find which data we need
  idg=list(set(idg23).intersection(set(idg1)))
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

def getdrift_raw_range_latlon(filename,id3,interval,datetime_wanted_1,num,step_size):
    
# this is for plot all the data in same range of lat and lon. id3 means int format of drift number
#'interval' means range of time, 'num' means how many pictures we will get
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
      time1.append(date2num(datetime.datetime.strptime(str(int(h[i]))+' '+str(int(day[i]))+' '+str(int(month[i]))+' '+str(int(year[i])), "%H %d %m %y")))


  idg1=list(ml.find(idd==id3))
  idg2=list(ml.find(np.array(time1)<=datetime_wanted_1+step_size/24.0*(num-1)+0.25))
  "'0.25' means the usual Interval, It can be changed base on different drift data "
  idg3=list(ml.find(np.array(time1)>=datetime_wanted_1-interval/24.0))
  idg23=list(set(idg2).intersection(set(idg3)))
  # find which data we need
  idg=list(set(idg23).intersection(set(idg1)))
 # print len(idg),len(set(idg))  
  lat,lon,time=[],[],[]
  
  for x in range(len(idg)):
      lat.append(round(lat1[idg[x]],4))
      lon.append(round(lon1[idg[x]],4))
  maxlon=max(lon)
  minlon=min(lon)
  maxlat=max(lat)
  minlat=min(lat)     
  # time is num
  return maxlon,minlon,maxlat,minlat
def hexcolors(n):
    """Compute a list of distinct colors, each of which is represented as an #RRGGBB value."""
    """It's useful for less than 100 numbers"""
    if pow(n,float(1)/3)%1==0.0:
        n+=1 
	  #make sure number we get is more than we need.
    rgbcolors=[]
    x=pow(n,float(1)/3)
    a=int(x)
    b=int(x)
    c=int(x)
    if a*b*c<=n:
       a+=1
    if a*b*c<n:
       b+=1
    if a*b*c<n:
       c+=1
    for i in range(a):
       r=254/(a)*(i)
       for j in range(b):
          s=254/(b)*(j)
          for k in range(c):
             t=254/(c)*(k)
             color=r,s,t
             rgbcolors.append(color)
    hexcolor=[]
    for i in rgbcolors:
        hexcolor.append('#%02x%02x%02x' % i)         
    return hexcolor
def point_in_poly(x,y,poly):  #judge whether a site is in or out a polygon 

    n = len(poly)
    inside = False

    p1x,p1y = poly[0]
    for i in range(n+1):
        p2x,p2y = poly[i % n]
        if y > min(p1y,p2y):
            if y <= max(p1y,p2y):
                if x <= max(p1x,p2x):
                    if p1y != p2y:
                        xints = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xints:
                        inside = not inside
        p1x,p1y = p2x,p2y

    return inside
def hexcolors(n):
    """Compute a list of distinct colors, each of which is represented as an #RRGGBB value."""
    """It's useful for less than 100 numbers"""
    if pow(n,float(1)/3)%1==0.0:
        n+=1 
	  #make sure number we get is more than we need.
    rgbcolors=[]
    x=pow(n,float(1)/3)
    a=int(x)
    b=int(x)
    c=int(x)
    if a*b*c<=n:
       a+=1
    if a*b*c<n:
       b+=1
    if a*b*c<n:
       c+=1
    for i in range(a):
       r=254/(a)*(i)
       for j in range(b):
          s=254/(b)*(j)
          for k in range(c):
             t=254/(c)*(k)
             color=r,s,t
             rgbcolors.append(color)
    hexcolor=[]
    for i in rgbcolors:
        hexcolor.append('#%02x%02x%02x' % i)         
    return hexcolor
