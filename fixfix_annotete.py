# -*- coding: utf-8 -*-
"""
Created on Tue Sep 22 12:10:32 2015

@author: hxu
"""

## STEPS ARE AS FOLLOWS:
#  - load all the ascii data file
#  - for each drifter it conducts 4 basic steps
#    - eliminate repeat times
#    - calculate forward and backward differences (velocity) and eliminate bad points
#    - writes meta data to log file
#    - check for drogue loss
#    - clean plots of track (pth) and velocity uv_id_final.png)
#  - generates oracle ready ascii file
##################################################################################################
import urllib
import sys
sys.path.append("/home3/ocn/jmanning/py/mygit/modules/")
import csv
from  conversions import ll2uv,distance #To convert from longitude/latitude to unit vectors
import numpy as np
import matplotlib as mpl
import matplotlib.mlab as ml
from datetime import datetime as dt
from pylab import *
import matplotlib.pyplot as plt
import basemap
from matplotlib.dates import num2date,date2num, DateFormatter
import math
import os
from mpl_toolkits.basemap import Basemap
critfactor=8 #multiple of the mean velcity to discard
minla=-20;maxla=70;minlo=-150;maxlo=20  # delimiting data to make it easier (we probably will not change this ever)
bathy=True # set to "True" if isobaths are wanted
timetoedit=5 #number of seconds to click on bad points (set to 10 first run through)
fn='drift_scotland_2015_1.dat'
#fn='drift_tcs_2014_1.dat'
testfile = urllib.URLopener()
testfile.retrieve("http://www.nefsc.noaa.gov/drifter/"+fn, fn)
fidids=open("/home/hxu/github/drifter/"+fn,"a")
fid=open("/home/hxu/github/drifter/drift.log","a")
#fidids=open("/data5/jmanning/drift/drift2header_sep2015.dat","a") # list of ids processed needed for making header
#fid=open("/home3/ocn/jmanning/drift/drift.log","a")#permanent log file that is appended to../home3/ocn/jmanning/drift/drift.log

# load /data5/jmanning/drift/massdmf/withtemp_2009.dat   ##ids with temperature
#list(set(line.strip() for line in open('X:/drift/bowdoin/2009/withtemp_2009.dat'))) # ids with temperature
#fileformat='bowdoin'; # format of temperature data (sometimes "emolt") if using minilog/dat files
#wt='withtemp_2009'

direcin="/home/hxu/github/drifter/" # directory where the final plots are stored
newpath = r'/home/hxu/github/drifter/'+fn[6:-11]+'/'+fn.split('_')[2] 
if not os.path.exists(newpath): os.makedirs(newpath)

direcout='/home/hxu/github/drifter/'+fn[6:-11]+'/'+fn.split('_')[2]
#direcout='/net/data5/jmanning/drift/tcs/2014'

fid.write('\n'+'#'*40+' below is '+str(fn)+' log '+'#'*40+'\n') # start new section in log file
depcont=[-100] # depth contour in final plot (apparently not used in 5/2012)
year=int(fn.split('_')[2])
year1=year # this does not get incremented
strattle=0 # this will eventually flag to "1" if yeardays change by more than 365
### END HARDCODES ################################################

####Function start ###############################################
def draw_basemap(fig, ax, lonsize, latsize, interval_lon, interval_lat):
    ax = fig.sca(ax)
    '''
    dmap = Basemap(projection='cyl',
                   llcrnrlat=min(latsize)-0.01,
                   urcrnrlat=max(latsize)+0.01,
                   llcrnrlon=min(lonsize)-0.01,
                   urcrnrlon=max(lonsize)+0.01,
                   resolution='h',ax=ax)
    '''
    dmap = Basemap(projection='cyl',
                   llcrnrlat=min(latsize)-(max(latsize)-min(latsize))/6,
                   urcrnrlat=max(latsize)+(max(latsize)-min(latsize))/6,
                   llcrnrlon=min(lonsize)-(max(lonsize)-min(lonsize))/6,
                   urcrnrlon=max(lonsize)+(max(lonsize)-min(lonsize))/6,
                   resolution='h',ax=ax)
               
    dmap.drawparallels(np.arange(int(min(latsize)),
                                 int(max(latsize))+1,interval_lat),
                       labels=[1,0,0,0], linewidth=0.1,fontsize=20)
    dmap.drawmeridians(np.arange(int(min(lonsize))-1,
                                 int(max(lonsize))+1,interval_lon),
                       labels=[0,0,0,1], linewidth=0.1,fontsize=20)
    dmap.drawcoastlines()
    dmap.fillcontinents(color='grey')
    #dmap.etopo()
    dmap.etopo()
    #dmap.warpimage()
def closest_node(node, nodes):
    nodes = np.asarray(nodes)
    deltas = nodes - node
    dist_2 = np.einsum('ij,ij->i', deltas, deltas)
    return np.argmin(dist_2)

def textxy(y1,x1,y2,x2,c):
    x3=(y2-y1)*c/(np.sqrt(np.square(x2-x1)+np.square(y2-y1)))
    y3=(x2-x1)*c/(np.sqrt(np.square(x2-x1)+np.square(y2-y1)))
    return y3,-x3



######end  functions ###############################
#raw data loaded
idss,yeardays_all,lat_all,lon_all,mths_all,days_all,hours_all,minutes_all,depths,temps=[],[],[],[],[],[],[],[],[],[]

csv_reader=csv.reader(open(direcin+fn,"r"))

for line in (x for x in csv_reader if x[0][0] !='%'):  # if the first line is comment line, skip
    # only parse the data if is has reasonable lat & lon according to the hardcoded minlo, maxlo, minla,maxla
    if float(line[0].split()[8])<maxla and float(line[0].split()[8])>minla and float(line[0].split()[7])>minlo and float(line[0].split()[7])<maxlo:
        idss.append(line[0].split()[0])
        yeardays_all.append(line[0].split()[6])
        lat_all.append(line[0].split()[8])
        lon_all.append(line[0].split()[7])
        mths_all.append(line[0].split()[2])
        days_all.append(line[0].split()[3])
        hours_all.append(line[0].split()[4])
        minutes_all.append(line[0].split()[5])
        depths.append(line[0].split()[9])
        temps.append(line[0].split()[10])
id=list(set(idss))

# convert string to float and int
yeardays_all=[float(i)+1 for i in yeardays_all]# in python num2date(), less one day than matlab, so add 1 here
lat_all=[float(i) for i in lat_all]
lon_all=[float(i) for i in lon_all]
mths_all=[int(i) for i in mths_all]
days_all=[int(i) for i in days_all]
hours_all=[int(i) for i in hours_all]
minutes_all=[int(i) for i in minutes_all]
idss=[int(i) for i in idss]
id=[int(i) for i in id]
  
fido=open(direcout+'/prep_for_oracle_'+fn[6:],'w')

ids=np.sort(id)



for k in range(len(ids)): #where "ids" is a sorted list of distinct ids and int
    # latitude, longitude, time
    strattle=0
    year=year1 # assumes all units from this batch start at the same year
    lat,lon,time,yeardays,depth,temp=[],[],[],[],[],[]
    #fidids.write(str(ids[k])+'\n') # writes to a list of ids needed in drifter header step
    for i in range(len(idss)):
        if int(float(idss[i]))==ids[k]:
            lat.append(lat_all[i])
            lon.append(lon_all[i])
            if (i>1)&(strattle==0):# here's where we account for a new year
                if yeardays_all[i]-yeardays_all[i-1]<-200:
                   year=year+1
                   print 'incremented year to '+str(year)
                   strattle=1
            yeardays.append(yeardays_all[i])
            #time.append(date2num(num2date(yeardays_all[i]).replace(year=year))) # this line was causing leapyear trouble in 2012
            time.append(date2num(dt(year,mths_all[i],days_all[i],hours_all[i],minutes_all[i],0)))
            depth.append(depths[i])
            temp.append(temps[i])
    print "there are ", len(lat), " fixes for id =",ids[k]          
    print "Note: Check to see if any of these already exist in database before loading"

    # STEP 1a: check for repeat time
    ###### while time[i]==time[i-1], get the del_same_time_index ########
    del_same_time_index=[]
    if len(time)>2:
     for i in range(1,len(time)):
        if int(time[i-1])==int(time[i]) and num2date(time[i-1]).hour== num2date(time[i]).hour and  num2date(time[i-1]).minute== num2date(time[i]).minute:
            del_same_time_index.append(i)
     del_same_time_index.reverse()
     if del_same_time_index==[]:
        print "there is no cases of repeat times."
     else:
        print str(len(del_same_time_index))+' points deleted with the same times'
        fid.write('   '+str(len(del_same_time_index))+' points deleted with the same times'+'\n')
        index=range(len(time))
        for i in del_same_time_index:    # remove repeat values
            del lat[i],lon[i],time[i],yeardays[i],depth[i],temp[i]
     forward_u,forward_v,forward_spd,jdn=ll2uv(time,lat,lon)# was yeardays but now uses "time" as of 3/29/2012
     backward_u,backward_v,backward_spd,backward_jdn=ll2uv(time[::-1],lat[::-1],lon[::-1])   #get speed data

     ## calculate resultants
     id_fs=list(np.where(np.array(forward_spd)<500)[0])   
     id_bs=list(np.where(np.array(backward_spd)<500)[0])
     idc=[val for val in id_fs if val in id_bs]
     jdraw,spdraw=[],[]
     for i in idc:
        jdraw.append(jdn[i])
        spdraw.append(forward_spd[i])
    
     # calculate a reasonable criteria for this drifter
     crit=np.mean([abs(i) for i in forward_spd])*critfactor
     print "Velocity criteria set to ", str(critfactor),' times the mean or ',str(crit),' cm/s'
     # check for drifter going aground (ie very low velocity)
     idlow=list(np.where(np.array(spdraw)<float(np.mean([abs(i) for i in forward_spd]))/100)[0])#calculate ids where velocity is less that 100 times the mean and print warning of "grounding"
     # if idlow is not empty, add the comments in fid file
     if idlow<>[]:
        for i in range(len(idlow)):
            print 'WARNING: Drifter ',str(ids[k]),' may be hung up on gear or aground on ',str(idlow[i]),' where velocity is < 1# mean'
            #fid.write(str(ids[k]).rjust(10)+' apparently hung-up on '+str(idlow[i])+'\n')
        idlow_print0=str(sorted(idlow))
        idlow_print1=idlow_print0.replace(', ',' ')
        tempochunk0=str(ids[k]).rjust(10)+' apparently hung-up on '+str(idlow_print1)+'\n'#'from'+str(idlow[0])+'to'+str(idlow[-1])+'\n'
     else:
        tempochunk0='There is no point hung up\n'


     #### find bad velocities where criteria was just calculated
     idbadf=list(np.where(abs(np.array(forward_spd))>crit)[0])
     idbadb=list(np.where(abs(np.array(backward_spd))>crit)[0])
    
     #if it is the 2nd time/point in the bad forward velocity (fu) that caused the problem
     # then the 2nd time/point associated with the bad backward velocity should match
     timeb=time[::-1] # backwards time vector
     badtime=list(set([time[i+1] for i in idbadf]).intersection(set([timeb[i+1] for i in idbadb])))
     print "%10.3f percent bad velocities deleted according to velocity criteria" % float(len(badtime)/float(len(lat))*100.)            
     index_badtime=[]# find near the badtime points
     for i in badtime:
        index_badtime.append(int(np.interp(i,time,range(len(time)))))
     if index_badtime<>[]:
      index_badtime.reverse()
      for i in index_badtime:
        index_near_badtimes=[]
        if i-5<0: 
            ra=range(0,i+5)
        elif i+5>len(lat):
            ra=range(i-5,len(lat)-1)
        else:
            ra=range(i-5,i+5)
        for m in ra:
            index_near_badtimes.append(m)
        plot_badtime=list(set(index_near_badtimes))
        #plot the bad time data and near the bad time data's points
        #plt.plot([lon[l] for l in plot_badtime],[lat[l] for l in plot_badtime],marker='.',)
        #plt.plot([lon[l] for l in index_badtime],[lat[l] for l in index_badtime],marker='o',markerfacecolor='r',linestyle='None')
        fig=plt.figure() 
        plt.plot([lon[l] for l in plot_badtime],[lat[l] for l in plot_badtime],marker='.',)
        plt.plot(lon[i],lat[i],marker='o',markerfacecolor='r',linestyle='None')
        thismanager = plt.get_current_fig_manager()
        thismanager.window.setGeometry(50,100,640, 545)
        #thismanager.frame.Maximize(True)
        #thismanager.window.SetPosition((2000, 0))
        plt.title(str(ids[k]))
        plt.show()
        #plt.close()
        del_or_not=raw_input('Delete? (y/n or 1 for the end point): ')
        if del_or_not=='y':
           del time[i],lat[i],lon[i],yeardays[i],depth[i],temp[i]
        elif del_or_not=='1':
           plt.plot(lon[i-1],lat[i-1],marker='o',markerfacecolor='r',linestyle='None')
           thismanager = plt.get_current_fig_manager()
           thismanager.window.SetPosition((2000, 0))
           plt.show()
           raw_input('How is that? press return')
           del time[i-1],lat[i-1],lon[i-1],yeardays[i-1],depth[i-1],temp[i-1]  
           plt.close()
        plt.close() 
        
        
     idgood=len(lat)
     fu,fv,spd1,jd1=ll2uv(time,lat,lon)
     jd1=[i/1000. for i in jd1 ]
     fig=plt.figure()
     #plot_speed(jd1,spd1)
     plt.plot(jd1,spd1)
     plt.plot(jd1,spd1,marker="o",markerfacecolor="r",linestyle='None')
     thismanager = plt.get_current_fig_manager()
     thismanager.window.setGeometry(50,100,640, 545)
     #thismanager.window.SetPosition((2000, 0))
     #thismanager.frame.Maximize(True)
     plt.title(str(ids[k]))
     plt.show()
     print 'click on any obviously bad points and then press the enter key. You have '+str(timetoedit)+' seconds.'
     badpoints=ginput(n=0,timeout=timetoedit)
     print badpoints#,timeout=10)
     index_badpoints=[]
     plt.close()
     badpoints_num=len(badpoints)
     if badpoints_num<>0:
       if badpoints[0][0]<jd1[0]: # where the first velocity is bad
          index_badpoints.append(badpoints[0][0])
       for i in range(badpoints_num):
#          index_badpoints.append(int(np.interp(badpoints[i][0],jd1,range(len(jd1))))) # where "jd1" is the datetime of velocity
           index_badpoints.append(closest_node(badpoints[i], zip(jd1,spd1)))  # get closest point in 2 dimensions
       print index_badpoints     
       print "%10.2f percent bad velocities deleted according to manual clicks on velocity" % float(float(badpoints_num)/len(lat)*100.)
     
       for i in sorted(index_badpoints)[::-1]:
          if i <=4: # delete points which in the boat or shore
          #drift_p.append([time[i], lat[i], lon[i], yeardays[i],depth[i],temp[i]])   
               del time[:i+1], lat[:i+1], lon[:i+1], yeardays[:i+1],depth[:i+1],temp[:i+1]
          #del time[i-1], lat[i-1], lon[i-1], yeardays[i-1],depth[i-1],temp[i-1]
       #plt.close()
     
        
       plot_again=raw_input("Do you want to replot the figure after delete the bad points? [note:say default y if you plan to specify a range]") or "y"
       #plot_again='y'
       if plot_again=="y" or plot_again=="Y" or plot_again=="yes":
          #plt.close('all')
          fig=plt.figure()
          fu2,fv2,spd2,jd2=ll2uv(time,lat,lon)
          #plot_speed(jd2,spd2)
          plt.plot(jd2,spd2,'mo-',markersize=5)#marker='o',markerfacecolor="r",linestyle='None')
          thismanager = plt.get_current_fig_manager()
          #thismanager.window.SetPosition((2000, 0))
          thismanager.window.setGeometry(50,100,640, 545)        
          plt.title(str(ids[k]))
          plt.show()     

       del_between=raw_input('Do you want to delete all the points between two points? [default n]') or "n"
       #del_between='N'
       if del_between=="N" or del_between=="n":
          print "You have choosen NOT to delete all the points between two points."
       if del_between=="Y" or del_between=="y" :
          print "Please click the first bad point and the last bad point to choose the range of the bad points"
          thismanager = plt.get_current_fig_manager()
          #thismanager.frame.Maximize(True)
          between_badpoints=ginput(n=2)
          print between_badpoints#,timeout=0)#,mouse_stop=2)
          index_between_badpoints=[]
          for i in range(len(between_badpoints)):
              index_between_badpoints.append(int(np.interp(between_badpoints[i][0],jd2,range(len(jd2)))))
          print index_between_badpoints
          index_betweens=[]
          for i in range(sorted(index_between_badpoints)[0],sorted(index_between_badpoints)[1]+1):
              index_betweens.append(i)
          for i in index_betweens[::-1]:
              del lat[i],lon[i],time[i],yeardays[i],depth[i],temp[i]
          del_between_badpoints=sorted(index_between_badpoints)[1]-sorted(index_between_badpoints)[0]+1
          badpoints_num=len(badpoints)+del_between_badpoints
          print "%10.2f percent editted due to bad velocities from manual clicks between two points" % float(float(badpoints_num)/len(time)*100.)
    
     if ids[k]==1174306915 or ids[k]==1174306911:
        del time[-1], lat[-1], lon[-1], yeardays[-1],depth[-1],temp[-1] 
        
     fig=plt.figure()
     fu3,fv3,spd3,jd3=ll2uv(time,lat,lon)
     #plot_speed(jd3,spd3)
     plt.plot(jd3,spd3,'bo-')  
     thismanager = plt.get_current_fig_manager()
     #thismanager.window.SetPosition((2000, 0))
     thismanager.window.setGeometry(50,100,640, 545)     
     plt.title(str(ids[k]))
     plt.show()
     print 'pausing for '+str(timetoedit)+' seconds'
     pause(1)
     plt.close()


     #step 5a:
     #manually delete points based on track
     
     fig=plt.figure()
     #plt.figure(2)
     #plt.plot(lon,lat,'k-')
     plt.plot(lon,lat,'ro-')
     thismanager = plt.get_current_fig_manager()
     #thismanager.frame.Maximize(True)
     #thismanager.window.SetPosition((2000, 0))
     thismanager.window.setGeometry(50,100,640, 545)     
     plt.title(str(ids[k]))
     plt.show()
     del_between=raw_input('Do you want to delete the points? [default n]') or "n"
     badplotpts=[] 
     if del_between=="Y" or del_between=="y":
       print 'click on any obviously bad points and then press the enter key on the track. You have '+str(timetoedit)+' seconds.'
       bad=ginput(n=0,timeout=timetoedit)
       print bad
       badplotpts=[] #index of points that are found to be near the same index of x & y
       if len(bad)>0:
         for kbad in range(len(bad)):
           fig=plt.figure()
           plt.plot(lon,lat,'ro-')
           ylim(bad[kbad][1]-.1,bad[kbad][1]+.1)
           xlim(bad[kbad][0]-.1,bad[kbad][0]+.1)
           thismanager = plt.get_current_fig_manager()
           thismanager.window.setGeometry(50,100,640, 545)
           plt.show()
         
           print 'click on any obviously bad points and then press the enter key. You have '+str(timetoedit)+' seconds.'
         
           bad1=ginput(n=1,timeout=timetoedit)
           badplotpts.append(closest_node(bad1, zip(lon,lat)))
           
       ylim(min(lat),max(lat))
       xlim(min(lon),max(lon))
       #for kk in range(len(badplotpts)):
       print '# bad pts'+str(len(badplotpts))
       for kj in badplotpts:
           plt.plot(lon[kj],lat[kj],'bo')
       thismanager = plt.get_current_fig_manager()
       thismanager.window.setGeometry(50,100,640, 545)  
      #thismanager.window.SetPosition((2000, 0))
       plt.show()
       print 'before and after length of pts'
       print 'before delete len='+str(len(lon))
       for i in sorted(badplotpts)[::-1]:
         plt.plot(lon[i],lat[i],'mo')
         del time[i], lat[i], lon[i], yeardays[i],depth[i],temp[i]
       print 'after delete len='+str(len(lon))
      
      #fig=plt.figure()
       plt.plot(lon,lat,'co-')
       thismanager = plt.get_current_fig_manager()
       thismanager.window.setGeometry(50,100,640, 545) 
      #thismanager.window.SetPosition((2000, 0))
       plt.show()
       raw_input(str(len(badplotpts))+' deleted from manual click on track. Press return to continue')  
       plt.close()


     # write to log file if some data was editted
     if badpoints_num>0:
          tempochunk1=(str(ids[k]).rjust(10)+' '+ str(crit).rjust(10)+' '+ str(badpoints_num).rjust(10)+' '+
                  str(idgood).rjust(10)+" "+str(math.floor(time[-1]-time[0])).rjust(10)+" manual editted uv plot\n")
     else:
          tempochunk1='There is no bad point delete manual.\n'
          
     if len(badtime)>0:
          tempochunk2=(str(ids[k]).rjust(10)+' '+ str(crit).rjust(10)+' '+ str(len(badtime)).rjust(10)+' '+
                  str(idgood).rjust(10)+" "+str(math.floor(time[-1]-time[0])).rjust(10)+" objectively editted\n")
     else:
          tempochunk2='There is no bad velocities deleted according to velocity criteria.\n'
              
     if len(badplotpts)>0:
          tempochunk3=(str(ids[k]).rjust(10)+' '+ str(crit).rjust(10)+' '+ str(len(badplotpts)).rjust(10)+' '+
                  str(idgood).rjust(10)+" "+str(math.floor(time[-1]-time[0])).rjust(10)+" manually editted track points\n")
     else:
          tempochunk3='There is no bad point delete manual on track.\n'

     # clean velocities w/out bad points
     [u2,v2,spd2,jd2]=ll2uv(time,lat,lon) #was "yeardays" until 3/2012 to deal with strattling new year

     #plot time, lat,lon
     fig=plt.figure()
     ax = fig.add_subplot(111)
     print 'skipping basemap_usgs using standard if big plot (>1 deg lat or lon range)'
     #print min(lat),min(lon),max(lat),max(lon)
     if (max(lon)-min(lon)>1) and (max(lat)-min(lat)>1) :
       #basemap.basemap_standard([int(min(lat)-1),int(max(lat))+1],[int(min(lon)-1),int(max(lon))+1],[1.0])#,(float(min(max(lat)-min(lat),max(lon)-min(lon)))+1.0)/5*4)
        if int(round((max(lon)-min(lon))/7))<=1:
            interval_lon=1
        else:
            interval_lon=int(round((max(lon)-min(lon))/7))
        if  int(round((max(lat)-min(lat))/7))<=1:
            interval_lat=1
        else:
            interval_lat=int(round((max(lat)-min(lat))/7))
            
        draw_basemap(fig, ax, lon, lat, interval_lon, interval_lat)
    #else:  
      #basemap.basemap_detail(lat,lon,bathy, False,float(min(max(lat)-min(lat),max(lon)-min(lon)))/5*4)
      #basemap.basemap_usgs(lat,lon,False)#,depcont)

     '''
     print 'past basemap'
     ax.plot(lon,lat,marker=".",markerfacecolor='r',markersize=10)
     points_num=10
     self_annotate1=ax.annotate("End", xy=(lon[-1], lat[-1]),xycoords='data', xytext=(-32, -32), 
                              textcoords='offset points',arrowprops=dict(arrowstyle="->"))
     self_annotate2=ax.annotate("Start", xy=(lon[0], lat[0]),xycoords='data', xytext=(-15, 28), 
                              textcoords='offset points',arrowprops=dict(arrowstyle="->"))
     
     xy_t=6  # xy_t: number of interval points between first points and current points, or current points and last points       
     len_arrow=1
     if time[-1]-time[0]<=2:
        if len(time)<5: skip=1
        else: skip=int(float(len(time))/5)
        for i in range(0,len(time),skip):
            if i <6 or i>(len(lon)-6): 
              self_annotate3=ax.annotate(num2date(time[i]).replace(tzinfo=None).strftime('%d-%b %H:%M'), xy=(lon[i], lat[i]),
                                      xycoords='data', xytext=(textxy(lon[i-1],lat[i-1],lon[i+1],lat[i+1],len_arrow)), textcoords='offset points',arrowprops=dict(arrowstyle="->"))
            else:
              self_annotate3=ax.annotate(num2date(time[i]).replace(tzinfo=None).strftime('%d-%b %H:%M'), xy=(lon[i], lat[i]),
                                      xycoords='data', xytext=(textxy(lon[i-xy_t],lat[i-xy_t],lon[i+xy_t],lat[i+xy_t],len_arrow)), textcoords='offset points',arrowprops=dict(arrowstyle="->"))  
              #print textxy(lon[i-xy_t],lat[i-xy_t],lon[i+xy_t],lat[i+xy_t],len_arrow)
     #     self_annotate3.draggable()
     elif (time[-1]-time[0]>2.0)&(time[-1]-time[0]<20.0):
        for i in range(1,len(time)):
            if num2date(time[i-1]).day<>num2date(time[i]).day:
                if i <6 or i>(len(lon)-6): 
                    self_annotate4=ax.annotate(num2date(time[i]).replace(tzinfo=None).strftime('%d-%b'), xy=(lon[i], lat[i]),
                                           xycoords='data', xytext=(lon[i]+textxy(lon[i-1],lat[i-1],lon[i+1],lat[i+1],len_arrow)[1],lat[i]+textxy(lon[i-1],lat[i-1],lon[i+1],lat[i+1],len_arrow)[1]), textcoords='data',arrowprops=dict(arrowstyle="->"))
                else:
                    self_annotate4=ax.annotate(num2date(time[i]).replace(tzinfo=None).strftime('%d-%b'), xy=(lon[i], lat[i]),
                                          xycoords='data', xytext=(lon[i]+textxy(lon[i-xy_t],lat[i-xy_t],lon[i+xy_t],lat[i+xy_t],len_arrow)[1],lat[i]+textxy(lon[i-xy_t],lat[i-xy_t],lon[i+xy_t],lat[i+xy_t],len_arrow)[0]), textcoords='data',arrowprops=dict(arrowstyle="->"))  
                    #print textxy(lon[i-xy_t],lat[i-xy_t],lon[i+xy_t],lat[i+xy_t],len_arrow)    
     else: # place approximately 10 labels
        for i in range(1,len(time),int(len(time)/10.)):
           #if num2date(time[i-1]).day<>num2date(time[i]).day:
           if i <6 or i>(len(time)-6): 
               self_annotate4=ax.annotate(num2date(time[i]).replace(tzinfo=None).strftime('%b-%d'), xy=(lon[i], lat[i]),
                                          xycoords='data', xytext=(lon[i]+textxy(lon[i-1],lat[i-1],lon[i+1],lat[i+1],len_arrow)[1],lat[i]+textxy(lon[i-1],lat[i-1],lon[i+1],lat[i+1],len_arrow)[1]), textcoords='data',arrowprops=dict(arrowstyle="->"))          #      self_annotate4.draggable() #drag the text if you want
           else:
               self_annotate4=ax.annotate(num2date(time[i]).replace(tzinfo=None).strftime('%b-%d'), xy=(lon[i], lat[i]),
                                          xycoords='data', xytext=(lon[i]+textxy(lon[i-xy_t],lat[i-xy_t],lon[i+xy_t],lat[i+xy_t],len_arrow)[1],lat[i]+textxy(lon[i-xy_t],lat[i-xy_t],lon[i+xy_t],lat[i+xy_t],len_arrow)[0]), textcoords='data',arrowprops=dict(arrowstyle="->"))    
               print textxy(lon[i-xy_t],lat[i-xy_t],lon[i+xy_t],lat[i+xy_t],len_arrow),time[i]
     
     '''
     print 'past basemap'
     ax.plot(lon,lat,marker=".",markerfacecolor='r',markersize=10)
     points_num=10
     self_annotate1=ax.annotate("End", xy=(lon[-1], lat[-1]),xycoords='data', xytext=(-32, -32), 
                              textcoords='offset points',arrowprops=dict(arrowstyle="->"))
     self_annotate2=ax.annotate("Start", xy=(lon[0], lat[0]),xycoords='data', xytext=(-15, 28), 
                              textcoords='offset points',arrowprops=dict(arrowstyle="->"))
     if time[-1]-time[0]<=2:
        if len(time)<5: skip=1
        else: skip=int(float(len(time))/5)
        for i in range(0,len(time),skip):
            self_annotate3=ax.annotate(num2date(time[i]).replace(tzinfo=None).strftime('%d-%b %H:%M'), xy=(lon[i], lat[i]),
                                      xycoords='data', xytext=(8, 11), textcoords='offset points',arrowprops=dict(arrowstyle="->"))
       #     self_annotate3.draggable()
     elif (time[-1]-time[0]>2.0)&(time[-1]-time[0]<20.0):
        for i in range(1,len(time)):
            if num2date(time[i-1]).day<>num2date(time[i]).day:
                self_annotate4=ax.annotate(num2date(time[i]).replace(tzinfo=None).strftime('%d-%b'), xy=(lon[i], lat[i]),
                                          xycoords='data', xytext=(8, 11),color='black', textcoords='offset points',arrowprops=dict(arrowstyle="->"))
     else: # place approximately 10 labels
        for i in range(1,len(time),int(len(time)/10.)):
           #if num2date(time[i-1]).day<>num2date(time[i]).day:
           self_annotate4=ax.annotate(num2date(time[i]).replace(tzinfo=None).strftime('%d-%b'), xy=(lon[i], lat[i]),
                                          xycoords='data', xytext=(textxy(lon[i-1],lat[i-1],lon[i+1],lat[i+1],20)), color='grey', textcoords='offset points',arrowprops=dict(arrowstyle="->"))          #      self_annotate4.draggable() #drag the text if you want     
     thismanager = plt.get_current_fig_manager()
     thismanager.window.setGeometry(50,100,640, 545)  
     #thismanager.window.SetPosition((2000, 0))
     plt.title(str(ids[k]))
     plt.show()
     plt.savefig(newpath+'pth_'+str(ids[k])+'_final'+".ps")
     #plt.savefig(direcin+'pth_'+str(ids[k])+'_final'+".png")
     raw_input('press return to close final track window')
     plt.close()
     # plt.show()

     #plot u & v
     fig=plt.figure()
     ax1 = fig.add_subplot(111)
     plt.plot(jdn,forward_u,"r",label='raw eastward')
     plt.plot(jdn, forward_v,"b",label='raw northward')
     plt.plot(jd2,u2,"m",linewidth=2,label='final eastward')
     plt.plot(jd2,v2,"g",linewidth=2,label='final northward')
     leg=plt.legend()
     # leg.draggable()

     locator = mpl.dates.AutoDateLocator()
     ax1.xaxis.set_major_locator(locator)
     if len(jdn)<100:
        monthsFmt = DateFormatter('%b/%d %H:')
     else:
        monthsFmt = DateFormatter('%b/%d')
     ax1.xaxis.set_major_formatter(monthsFmt)
     ax1.set_xlabel(str(year))
     ax1.set_ylabel('cm/s (where 50 ~ 1 knot)')
     fig.autofmt_xdate()  #display the time "lean"
     plt.title('Drifter '+str(ids[k])+' cleaned',fontsize=16)
     #plt.savefig(direcin+'uv_'+str(ids[k])+'_final'+'.ps')
     #plt.savefig(direcin+'uv_'+str(ids[k])+'_final'+'.png')
     thismanager = plt.get_current_fig_manager()
     thismanager.window.setGeometry(50,100,640, 545)  
     #thismanager.window.SetPosition((2000, 0))
     plt.show()
     raw_input('press return to close uv window')
     plt.close()
     # close()

     # write out id,date,lat,lon,yrday0_gmt,temp, and depth_i

     depth=[float(i) for i in depth]
     for i in range(len(time)):     
        fido.write(str(ids[k]).rjust(10)+ " " +num2date(time[i]).replace(tzinfo=None).strftime('%d-%b-%Y:%H:%M')+" ")
        fido.write(("%10.6f") %(lat[i]))
        fido.write(" ")
        fido.write(("%10.6f") %(lon[i]))
        fido.write(" ")
        fido.write(("%10.6f") %(yeardays[i]-1))
        fido.write(" ")
        fido.write(temp[i]+ " ")
        fido.write(("%5.1f") %(depth[i]))
        fido.write('\n')
     if k<>len(ids)-1:        
      raw_input("Press Enter to process next drifter")  

     whetherlog=raw_input('Do you want to keep this log? [default=y]') or "y"
     if whetherlog=="Y" or whetherlog=="y" :
        fid.write(tempochunk0)
        fid.write(tempochunk1)
        fid.write(tempochunk2)
        fid.write(tempochunk3)
        print 'log has been saved.'
     else:
        print 'log discarded' 
fido.close()
fid.close()
fidids.close()
     