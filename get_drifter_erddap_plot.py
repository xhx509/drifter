# -*- coding: utf-8 -*-
"""
Created on Wed Aug 27 10:14:02 2014

@author: hxu
this progress extracts drifter data(coordinates) based on time range, geographic range or drifter id, then plot them.
The ouput file will be in same folder as this program. 
input values: time period,gbox(maxlon, minlon,maxlat,minlat),or time period and id
function uses: getobs_drift_byrange,getobs_drift_byidrange,colors,getobs_drift_byid
output : a plot file to show drifter track.

"""
from basemap import basemap_region
import datetime as dt
import sys
import os
import pytz, pylab
import numpy as np
import matplotlib.pyplot as plt
from drifter_functions import getobs_drift_byrange,getobs_drift_byidrange,colors,getobs_drift_byid
ops=os.defpath
pydir='../'
sys.path.append(pydir)
#################Input values#############################################
input_time=[dt.datetime(1977,1,1,0,0,0,0,pytz.UTC),dt.datetime(2015,7,1,0,0,0,0,pytz.UTC)] # start time and end time
gbox=[-70.0,-72.0,42.0,40.0] #  maxlon, minlon,maxlat,minlat
id=['55291', '    55292', '    55293', '    57202', '    65204', '    65205', '    65206', '    65291', '    65292', '    65293', '    65294', '    65295', '    66207', '    90301', '    90302', '    94303', '    94491', '    94492', '    95491', '    95492', '    97115', ' 97420703', ' 97420704', ' 97420705', ' 97420706', ' 97420707', ' 97420708', ' 97420709', ' 99361212', ' 99420701', ' 99420702', ' 99420703', ' 99420704', ' 99420705', ' 99420706', ' 99420707', ' 99420708', ' 99420709', '100240811', '100361211', '104420701', '1054207019', '1054207020', '105430681', '105430693', '105440671', '105440672', '105440673', '105440674', '105440675', '105440676', '105440681', '1054406810', '1054406811', '1054406812', '1054406813', '105440682', '105440683', '105440684', '105440685', '105440686', '105440687', '105440688', '105440689', '105470641', '105470644', '105470645', '105470646', '106280851', '106280871', '106290881', '106290882', '106290885', '106410702', '106410703', '106410704', '106410706', '106410707', '106410708', '106410709', '106410712', '106420701', '106420702', '106420703', '106420704', '106430691', '106430692', '106430693', '106430701', '106440681', '106440682', '106440683', '107410701', '107410702', '107410703', '107410704', '107410705', '107420701', '1074207010', '1074207011', '1074207012', '107420705', '107420708', '107430691', '107440671', '107440672', '108240811', '108410712', '108430701', '108430702', '1084406710', '1084406711', '109290841', '109290881', '109290885', '109430701', '109430702', '43202', '45380', '453810', '453812', '453813', '453814', '453815', '453816', '453817', '453818', '453819', '45382', '45384', '45386', '45388', '46202', '46382', '46392', '46472', '47202', '47205', '47362', '47382', '47392', '47472', '48202', '48382', '48392', '48472', '49202', '49382', '49392', '49472', '54291', '54292', '55201', '55202', '55203', '55381', '55382', '55383', '55384', '55385', '55386', '56101', '56202', '60301', '60391', '60392', '66201', '66202', '66203', '66204', '66205', '66381', '66382', '66383', '66384', '66385', '66386', '69391', '693910', '693912', '693914', '69393', '69395', '69397', '69399', '70391', '70392', '70395', '70398', '75201', '75202', '75203', '75291', '75292', '75293', '75294', '75295', '75296', '75381', '75382', '75383', '75384', '75385', '75386', '76201', '76202', '76203', '76381', '76382', '76383', '76384', '76385', '76386', '79394', '79395', '79396', '80201', '80301', '80302', '80303', '80304', '80305', '80393', '80394', '80397', '82371', '82372', '82373', '82374', '82375', '82376', '85201', '85202', '85203', '85291', '85292', '85301', '85302', '85303', '85304', '85391', '85392', '85393', '85394', '85395', '85396', '85397', '85398', '85399', '86091', '86301', '87171', '87201', '87301', '87302', '87303', '87304', '88201', '88202', '88461', '88462', '88463', '89301', '89302', '89393', '89394', '89398', '91191', '96101', '96102', '96104', '96105', '96107', '96108', '96111', '96112', '96113', '96114', '96201', '96301', '96302', '96303', '97101', '971010', '97102', '97103', '97104', '97105', '97106', '97107', '97108', '97109', '97111', '97112', '97113', '97114', '97201', '97202', '97301', '97302', '974207010', '974207011', '974207012', '98101', '98102', '98103', '98104', '98105', '98201', '98301', '98302', '99301', '994207010', '994207011', '994207012', '994207013', '994207014', '994207015', '994207016', '994207017', '994207018'] # id list, if you are not clear dedicated id, let id=[]
#'125450842''125450841'
#↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑Input values↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑#
id=[int(a) for a in id]
fig = plt.figure()
ax = fig.add_subplot(111)  

if id==[]:
    
    time,ids,lats,lons=getobs_drift_byrange(gbox,input_time)
    id=list(set(ids))
    rgbcolors=colors(len(id))
    for k in range(len(id)):
        time,ids,lat,lon=getobs_drift_byidrange(id[k],gbox,input_time)
        plt.plot(lon[0],lat[0],'.',markersize=30,color=rgbcolors[k+1],label=str(id[k]))
        plt.plot(np.reshape(lon,np.size(lon)),np.reshape(lat,np.size(lat)),color=rgbcolors[k+1])
else:
    lats,lons=[],[]
    rgbcolors=colors(len(id))
    for m in range(len(id)):
        time,ids,lat,lon=getobs_drift_byid(id[m],input_time)
        plt.plot(lon[-1],lat[-1],'.',markersize=30,color=rgbcolors[m+1],label=str(id[m]))
        plt.plot(np.reshape(lon,np.size(lon)),np.reshape(lat,np.size(lat)),color=rgbcolors[m+1])
        for n in range(len(lat)):  
            lats.append(lat[n])
            lons.append(lon[n])
basemap_region('ne')    
    
plt.title(str(time[0].strftime("%d-%b-%Y %H"))+'h') 
    
pylab.ylim([min(lats)-(max(lats)-min(lats))/6.0,max(lats)+(max(lats)-min(lats))/6.0])
pylab.xlim([min(lons)-(max(lons)-min(lons))/6.0,max(lons)+(max(lons)-min(lons))/6.0])

ax.patch.set_facecolor('lightblue')   #set background color

plt.legend( numpoints=1,loc=2)  
#plt.savefig('./'+dt.datetime.now().strftime('%Y-%m-%d %H:%M') + '.png')
 
#datetime_wanted=date2num(num2date(datetime_wanted)+datetime.timedelta( 0,step_size*60*60 ))
plt.show()
