# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 14:42:11 2013

@author: hxu

this is a control file , user could import data from here
"""


from matplotlib.dates import num2date,date2num

import datetime as dt
def getcodar_ctl_file_py():
   dtime='2013,6,3,8,0'  #time like 2012,8,31,17,0
   filename=['http://www.nefsc.noaa.gov/drifter/drift_patriot_2013_2.dat']  # raw drifter filename
   drifternumber=['136410701']  #drift number like 128380741
   num_interval=[1,50,50] #the num of picture, Time Interval (for the case of overlays option 5, it means total time of track in hour), step size (in the case of option 5, this is not read)
   model_option=[5]  #choose one url to get codar
#1,http://tashtego.marine.rutgers.edu:8080/thredds/dodsC/cool/codar/totals/macoora6km_fmrc/Macoora_6km_Totals_(FMRC)_best.ncd" 
#2,http://tashtego.marine.rutgers.edu:8080/thredds/dodsC/cool/codar/totals/sw06" 
#3,http://tashtego.marine.rutgers.edu:8080/thredds/dodsC/cool/codar/totals/macoora6km"          
#4,http://tashtego.marine.rutgers.edu:8080/thredds/dodsC/cool/codar/totals/macoora8km"   
#5,http://tashtego.marine.rutgers.edu:8080/thredds/dodsC/cool/codar/totals/macoora6km_clone"


#This ctl file work with get_drifter,getsst_codar_drifter,gettrack_codar
  #dtime=dtime[0:dtime.index(']')].strip('[')
   datetime_wanted=date2num(dt.datetime.strptime(dtime,'%Y,%m,%d,%H,%M')) 
  
   filename=filename[0]

   drifternumber=drifternumber[0] 

   print 'number of frames, interval time (hours), step size (hours?) :'+str(num_interval)
   num=int(num_interval[0])
   interval=int(num_interval[1])
   interval_dtime=dt.timedelta( 0,interval*60*60 )
   step_size=int(num_interval[2])

   model_option=model_option[0]
  
   if model_option==1:
      url="http://tds.marine.rutgers.edu:8080/thredds/dodsC/cool/codar/totals/macoora6km_fmrc/Macoora_6km_Totals_(FMRC)_best.ncd" 
   if model_option==2:
      url="http://tds.marine.rutgers.edu:8080/thredds/dodsC/cool/codar/totals/sw06" 
   if model_option==3:
      url="http://tds.marine.rutgers.edu:8080/thredds/dodsC/cool/codar/totals/macoora6km"          
   if model_option==4:
      url="http://tds.marine.rutgers.edu:8080/thredds/dodsC/cool/codar/totals/macoora8km"   
   if model_option==5:
      url="http://tds.marine.rutgers.edu:8080/thredds/dodsC/cool/codar/totals/macoora6km_clone"
   if model_option=='6':
      url="http://tds.marine.rutgers.edu:8080/thredds/dodsC/cool/codar/totals/5Mhz_6km_realtime_fmrc/Maracoos_5MHz_6km_Totals-FMRC_best.ncd"  
   return datetime_wanted,filename,drifternumber,url,model_option,num,interval_dtime,interval,step_size