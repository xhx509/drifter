# -*- coding: utf-8 -*-
"""
Created on Thu Nov  5 13:05:56 2015
After you get file 'sqldump_header.dat', run this python program to get a dat file split by comma.


@author: hxu
"""
import pandas as pd
from bs4 import BeautifulSoup
import urllib
import datetime as dt
from matplotlib.dates import num2date,date2num
import sys
sys.path.append("/home3/ocn/jmanning/py/mygit/modules/")
from conversions import distance,dm2dd
#from pydap.client import open_url
import numpy as np
###################################
## HARDCODES
inputfile="sqldump_header_apr2016.dat"
outputfile="drift2header_apr2016.out"
##################################

def get_drifter_type(string):
    type_d=''
    drift_type=['irina','cassie','eddle','rachel']
    for i in drift_type:
        if string.lower().find(i)<>-1:
            type_d=i
    if  type_d=='':
        type_d='null'
    return type_d    

def get_w_depth(xi,yi):  #xi:lon  yi:lat
    url='http://geoport.whoi.edu/thredds/dodsC/bathy/gom03_v1_0'#url='http://geoport.whoi.edu/thredds/dodsC/bathy/crm_vol1.nc' ):
    if xi[0]>999.: # if it comes in decimal -minutes, conert it
        #for kk in range(len(xi)):
        (y2,x2)=dm2dd(yi[0],xi[0])
        yi[0]=y2
        xi[0]=x2
    try:    
        dataset = open_url(url)
        
    except:
        print 'Sorry, ' + url + ' is not available' 
        sys.exit(0)

    #read lat, lon,topo from url
    xgom_array = dataset['lon']
    ygom_array = dataset['lat']
    dgom_array = dataset['topo'].topo

    #print dgom_array.shape, xgom_array[5:9],dgom_array[5]

    #convert the array to a list
    xgom, ygom = [], []
    
    for i in xgom_array:
        if i > xi[0] - 0.00834 and i < xi[0] + 0.00834:
            xgom.append(i)
  
    for i  in ygom_array:
        if i > yi[0] - 0.00834 and i < yi[0] + 0.00834:
            ygom.append(i)


    x_index, y_index = [], []
    (ys, xs) = dgom_array.shape

    for i in range(0, len(xgom)):
        x_index.append(int(round(np.interp(xgom[i], xgom_array, range(xs)))))
    for i in range(0, len(ygom)):
        y_index.append(int(round(np.interp(ygom[i], ygom_array, range(ys)))))
    
    dep, distkm, dist1 = [], [], []

    for k in range(len(x_index)):
        for j in range(len(y_index)):
            dep.append(dgom_array[(y_index[j], x_index[k])])
       
            distkm, b = distance((ygom[j], xgom[k]), (yi[0], xi[0]))
            dist1.append(distkm)
    #print dist1        
    if len(dist1)>=3:    
      #get the nearest,second nearest,third nearest point.
      dist_f_nearest = sorted(dist1)[0]
      dist_s_nearest = sorted(dist1)[1]
      dist_t_nearest = sorted(dist1)[2]
    
      index_dist_nearest = range(len(dist1))
      index_dist_nearest.sort(lambda x, y:cmp(dist1[x], dist1[y]))
    
      dep_f_nearest = dep[index_dist_nearest[0]]
      dep_s_nearest = dep[index_dist_nearest[1]]
      dep_t_nearest = dep[index_dist_nearest[2]]

      #compute the finally depth
      d1 = dist_f_nearest
      d2 = dist_s_nearest
      d3 = dist_t_nearest
      def1 = dep_f_nearest
      def2 = dep_s_nearest
      def3 = dep_t_nearest
      depth_finally = def1 * d2 * d3 / (d1 * d2 + d2 * d3 + d1 * d3) + def2 * d1 * d3 / (d1 * d2 + d2 * d3 + d1 * d3) + def3 * d2 * d1 / (d1 * d2 + d2 * d3 + d1 * d3)
    else:
      depth_finally = np.array([[-9999]])
    return depth_finally
    

f = urllib.urlopen("http://www.nefsc.noaa.gov/drifter/index_2015.html")
f2= open(inputfile)           #you may need to change this path
data_raw=f2.readlines()
data_raw_id=[int(data_raw[s][:10]) for s in range(len(data_raw))] # list of  ids missing in header
html = f.read() # reads web page
soup = BeautifulSoup(html)
table = soup.find("table")
rows = table.findAll("tr")
soup_all=soup.find_all('a')     # convert html data to 
drift_html=[]
for i in range(len(soup_all)):
    if str(soup_all[i])[:15]=='<a href="drift_': 
       if str(soup_all[i]).split(">")[0][-2]=='v': # this finds csv file
           drift_html.append(str(soup_all[i]).split(">")[0][9:-1])
    
x = 0
tables=[]
for tr in rows:
    cols = tr.findAll("td")
    if not cols: 
        # when we hit an empty row, we should not print anything to the workbook
        continue
    y = 0
    for td in cols:
        texte_bu = td.text
        texte_bu = texte_bu.encode('utf-8')
        texte_bu = texte_bu.strip()
        tables.append(texte_bu)
tables=tables[9:] # get rid of the header line
data_all=[]
data_html=[]
for i in range(len(drift_html)):
    if tables[9*i+6]=='done':     #find the table that we need. 
        df=pd.read_csv('http://www.nefsc.noaa.gov/drifter/'+drift_html[i])
        if len(df)==0:
            continue
        print drift_html[i]
        data_all.append(list(df.iloc[0])) # gets first id
        # now get all the info about this deployment id
        data_html.append([tables[9*i],tables[9*i+1],tables[9*i+2],tables[9*i+3],tables[9*i+4],tables[9*i+5],get_drifter_type(tables[9*i+7]),tables[9*i+8],drift_html[i].split('_')[1]])
        for n in range(1,len(df)):
            if list(df.iloc[n])[0]<>list(df.iloc[n-1])[0]: # finds other id 
                data_all.append(list(df.iloc[n]))
                data_html.append([tables[9*i],tables[9*i+1],tables[9*i+2],tables[9*i+3],tables[9*i+4],tables[9*i+5],get_drifter_type(tables[9*i+7]),tables[9*i+8],drift_html[i].split('_')[1]])
lis=[] # distinct ids from the csv file
for x in range(len(data_all)):
    lis.append(int(data_all[x][0]))
num1=0
both_in_lis=[] 

for i in range(len(lis)):
    if lis[i] in data_raw_id: #where data_raw_id come from the sqldump file
        print 'in sqldump_header: '+str(lis[i])
        both_in_lis.append(lis[i])
        num1+=1
idd,lat_start,lon_start,start_date,deployer,institute,project,ndays,notes,esn,end_date,pi,yrday0_gmt,lat_end,lon_end,depth,drift_type,start_depth,manufacturer=[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]
dict_data_raw={}
for p in range(len(data_all)): # for each id we got from data files
    for q in range(len(data_raw_id)): # for each id we got from sqldump
        if lis[p]==data_raw_id[q]: # where "lis" is the integer version of data_all
            idd.append(lis[p])
            lat_start.append(data_raw[q][0:data_raw[q].index('\n')].split(' ')[4])
            lon_start.append(data_raw[q][0:data_raw[q].index('\n')].split(' ')[3])
            #start_depth.append(round(get_w_depth([float(data_raw[q][0:data_raw[q].index('\n')].split(' ')[3])],[float(data_raw[q][0:data_raw[q].index('\n')].split(' ')[4])])[0][0],1))
            start_depth.append('null')
            start_date.append(num2date(date2num(dt.datetime(int(data_raw[q][0:data_raw[q].index('\n')].split(' ')[1])+2000,1,1))+float(data_raw[q][0:data_raw[q].index('\n')].split(' ')[2])).strftime("%d-%b-%Y:%H%M"))
            deployer.append(data_html[p][1].split(' ')[0].split('/')[0])
            institute.append(data_html[p][8].upper())
            drift_type.append(data_html[p][6])
            #project.append
            ndays.append(round(float(data_raw[q][0:data_raw[q].index('\n')].split(' ')[6]),1))
            notes.append(data_html[p][-1].replace(",", ";"))
            try:
                esn.append(int(data_all[p][1])) # if there is no letters this try will work
                manufacturer.append('GLOBALSTAR')
            except:
                esn.append(data_all[p][1])
                manufacturer.append('IRIDIUM')
            end_date.append(data_raw[q][0:data_raw[q].index('\n')].split(' ')[-2])
            yrday0_gmt.append(data_raw[q][0:data_raw[q].index('\n')].split(' ')[2])
            lat_end.append(data_raw[q][0:data_raw[q].index('\n')].split(' ')[8])
            lon_end.append(data_raw[q][0:data_raw[q].index('\n')].split(' ')[7])
            depth.append(data_raw[q][0:data_raw[q].index('\n')].split(' ')[5])
            
f = open(outputfile, 'w')  
f.writelines('id'+','+'yrday0_gmt'+','+'lat_start'+','+'lon_start'+','+'depth_bottom'+','+'start_date'+','+'drogue_depth_start'+','+'drogue_depth_end'+','+'depth'+','+'project'+','+'institute'+','+'pi'+','+'deployer'+','+'type'+','+'manufacturer'+','+'communication'+','+'accuracy'+','+'esn'+','+'yeardays'+','+'notes'+' \n') 
#[f.writelines(str(idd[u])+','+str(lat_start[u])+','+str(lon_start[u])+','+str(start_date[u])+','+str(deployer[u])+','+str(institute[u])+','+str(ndays[u])+','+str(esn[u])+','+str(yrday0_gmt[u])+','+str(end_date[u])+','+str(lat_end[u])+','+str(lon_end[u])+','+str(depth[u])+','+str(notes[u])+','+'\n')  for u in range(len(esn))]
[f.writelines(str(idd[u])+','+str(yrday0_gmt[u])+','+str(float(lat_start[u])*100)+','+str(float(lon_start[u])*100)+','+str(start_depth[u])+','+str(start_date[u])+','+'null,'+'null,'+str(depth[u])+','+'null,'+str(institute[u])+','+'null,'+str(deployer[u])+','+str(drift_type[u])+','+str(manufacturer[u])+','+'null,'+'null,'+str(esn[u])+','+str(ndays[u])+','+str(notes[u])+','+'\n')  for u in range(1,len(esn))]
f.close() 

