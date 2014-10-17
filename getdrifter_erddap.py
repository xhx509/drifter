# -*- coding: utf-8 -*-
"""
Created on Mon Aug 18 13:19:58 2014

@author: hxu

it used for getting drifter data from erddap based on different conditions()
After running this program, you could get  a file of drifter data
The saving file will be in same folder as this program
input values: time period,gbox(maxlon, minlon,maxlat,minlat),ids
function uses:getobs_drift_byid, getobs_drift_byrange
output : a data file which includes ids, time, lat,lon
"""
import datetime as dt
import sys
import os
import pytz
from hx import getobs_drift_byrange,getobs_drift_byid
ops=os.defpath
pydir='../'
sys.path.append(pydir)
#################Input values#############################################
input_time=[dt.datetime(2013,1,1,0,0,0,0,pytz.UTC),dt.datetime(2013,7,1,0,0,0,0,pytz.UTC)] # start time and end time
gbox=[-70.0,-72.0,42.0,40.0] #  maxlon, minlon,maxlat,minlat
id=[135410701] # id list, if you are not clear dedicated id, let id=[]
'125450842''125450841'
#↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑Input values↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑#

f = open(str(gbox[3])+'.dat', 'w')  # create file and name it
f.writelines('id'+'                 '+'lat         '+' lon        '+'      time'+'   \n')
if id==[]:
    time,ids,lat,lon=getobs_drift_byrange(gbox,input_time)  #get  and organize data
    for k in range(len(ids)): # write them
       f.writelines(str(ids[k])+'    '+'%10.2f' % lat[k]+'   '+'%10.2f' % lon[k]+'   '+'      '\
       +str(time[k].strftime('%Y-%m-%d %H:%M:%S'))+'\n')
 
else:
    for q in range(len(id)):
        time,ids,lat,lon=getobs_drift_byid(id[q],input_time)  #get  and organize data
        for k in range(len(ids)): #write them
           f.writelines(str(ids[k])+'    '+'%10.2f' % lat[k]+'   '+'%10.2f' % lon[k]+'   '+'      '\
           +str(time[k].strftime('%Y-%m-%d %H:%M:%S'))+'\n')

f.close()


'''  
fig = plt.figure()
ax = fig.add_subplot(111)   
plt.title(str(time[0].strftime("%d-%b-%Y %H"))+'h')
lat_wanted=lat[-1]
lon_wanted=lon[-1]
plt.plot(lon_wanted,lat_wanted,'.',markersize=30,color='r',label='end')
  
    #plt.plot(np.reshape(lon,np.size(lon)),np.reshape(lat,np.size(lat)))
plt.plot(np.reshape(lon,np.size(lon)),np.reshape(lat,np.size(lat)),color='black')
    
  #basemap_usgs([minlat-1,maxlat+1],[minlon-1,maxlon+1],'True')
plt.plot(lon[0],lat[0],'.',markersize=20,color='g',label='start')  # start time
pylab.ylim([min(lat)-0.1,max(lat)+0.1])
pylab.xlim([min(lon)-0.1,max(lon)+0.1])
ax.patch.set_facecolor('lightblue')   #set background color

plt.legend( numpoints=1,loc=2)  
plt.savefig('./'+str(time[0].strftime("%d-%b-%Y %H"))+'h' + '.png')
 
#datetime_wanted=date2num(num2date(datetime_wanted)+datetime.timedelta( 0,step_size*60*60 ))
plt.show()
'''