# -*- coding: utf-8 -*-
"""
Created on Tue Aug 02 15:14:57 2016

@author: Xavier
"""
import pandas as pd
import datetime as dt
import glob
import linecache
import numpy
import ftplib
import os
import time
import urllib
from bs4 import BeautifulSoup


f = urllib.request.urlopen("http://www.nefsc.noaa.gov/drifter/")

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
drift_html=list(set(drift_html)) #get rid of the repeat csv url
drift_html.append('drift_X.csv')

gpx_not_exist=[] # gather not exist gpx file 
##############################################   Create gpx files for leaflet reading   ##################################################################
for csv in drift_html:

    try:
        #df_codes=pd.read_csv('/net/data5/jmanning/drift/codes.dat',sep='\s+',engine='python',names=['esn','ids','depth','teacher','school'])   # hard codes need to find codes.dat 
        df_codes=pd.read_csv('codes.dat',sep='\s+',engine='python',names=['esn','ids','depth','teacher','school'])
    
    #import matplotlib.pyplot as plt
        df=pd.read_csv('http://www.nefsc.noaa.gov/drifter/'+csv,index_col=[0])  # read drifter csv file
    except:
        print (csv)  
    office_name='_OurNOAAlab'
    office_lat=41.570270
    office_lon=-70.620188
    ############################################################################################################################################
    #
    
    names=df.index.unique().tolist() #get all  drifters' ID
    timestart=[]
    timeend=[]
    uschool=[];uteacher=[];udepth=[];deployid=[];esn=[];data=[]
    print (len(names))
    
    
    
        
    for x in range(len(names)): #for each drifter
        
            name=names[x]
            drifter=[]
            df1=df.loc[name]
            if type(df1.index[0])==numpy.int64:
             if int(str(df1.index[0])[:2])>=20: # this was HARDCODED to >=2016 but we change it on July 20, 2018 to 2017 and on July 29, 2020 to 2020

                        timestart.append((dt.datetime((2000+int(str(df1.index[0])[:2])),1,1,0,0)+dt.timedelta(df1.iloc[0][5])))
                        timeend.append((dt.datetime((2000+int(str(df1.index[0])[:2])),1,1,0,0)+dt.timedelta(df1.iloc[-1][5])))
                        q=0
                        for p in range(1,len(df1)):
                            if df1.iloc[p][5]<100 and df1.iloc[p-1][5]>300:
                                q=q+1
                        timeend.append((dt.datetime((2000+int(str(df1.index[0])[:2])+q),1,1,0,0)+dt.timedelta(df1.iloc[-1][5])))
                        for m in range(len(df_codes)): # for each drifter in codes.dat
                            if str(df_codes['ids'][m])==str(name):         #find corresponse name
                                if df_codes['school'][m]!=None and df_codes['school'][m] not in uschool:
                                
                                    uschool.append(str(df_codes['ids'][m])+'_'+df_codes['school'][m])  #create the name
                                    uteacher.append(df_codes['teacher'][m])
                                    udepth.append(df_codes['depth'][m])
                                    deployid.append(df_codes['ids'][m])
                                    esn.append(df_codes['esn'][m])
                                elif  df_codes['school'][m]!=None and df_codes['school'][m]  in uschool: #add "$" to end of school name
                                    uschool.append(df_codes['school'][m]+'$')
                                    uteacher.append(df_codes['teacher'][m])
                                    udepth.append(df_codes['depth'][m]) 
                                    deployid.append(df_codes['ids'][m])
                                    esn.append(df_codes['esn'][m])
                                elif df_codes['school'][m]==None:           # if there is no school name, add esn number to school name list
                                    uschool.append(str(df_codes['school'][m]))
                                    uteacher.append(' ')
                                    udepth.append(df_codes['depth'][m])   
                                    deployid.append(df_codes['ids'][m])
                                    esn.append(df_codes['esn'][m])
                                    
                                    
                                
                                if len(uschool[-1].split('$'))!=1:
                                    school_name=uschool[-1].split('$')[0]+'_'+str(len(uschool[-1].split('$'))) #add a count 1,2,3 etc to the schoolname
                                else:
                                    school_name=uschool[-1]
                                data.append(str(school_name)+'.gpx')
                                if not os.path.isfile(str(school_name)+'.gpx'): #create the gpx file if the gpx file is not exist
                                    gpx_not_exist.append((str(school_name)+'.gpx'))
                                    f=open(str(school_name)+'.gpx','w')
                                    #print 1
                                    
                                    f.writelines("<?xml version='1.0' encoding='UTF-8'?>\n")
                                    f.writelines("<gpx version='1.1' creator='drifter'\n")
                                    f.writelines("  xsi:schemaLocation='"+str(name)+','+str(school_name)+','+str(udepth[-1])+','+str(uteacher[-1])+','+str(deployid[-1])+','+str(esn[-1])+"'\n")
                                    f.writelines("  xmlns='http://www.topografix.com/GPX/1/1'\n")
                                    f.writelines("  xmlns:gpxtpx='http://www.garmin.com/xmlschemas/TrackPointExtension/v1'\n")
                                    f.writelines("  xmlns:gpxx='http://www.garmin.com/xmlschemas/GpxExtensions/v3' xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance'>\n")
                                    f.writelines("  <metadata>\n")
                                    f.writelines("    <link href='connect.garmin.com'>\n")
                                    f.writelines("      <text>drifter  data</text>\n")
                                    f.writelines("    </link>\n")
                                    f.writelines("    <time>2015-03-08T07:27:47.000Z</time>\n")
                                    f.writelines("  </metadata>\n")
                                    f.writelines("  <trk>\n")
                                    f.writelines("    <name>Xavier track</name>\n")
                                    f.writelines("    <trkseg>\n")
                                
                                
                                    k=0
                                    for x in range(len(df1)): # for each fix in this drifter
                                            if x>1:
                                                if df1.iloc[x][5]<100 and df1.iloc[x-1][5]>300:
                                                    k=k+1
                                             #drifter.append([dt.datetime((2000+int(str(df1.index[0])[:2])),1,1,0,0)+dt.timedelta(df1.iloc[x][5]),df1.iloc[x][6],df1.iloc[x][7]])
                                            f.writelines('      <trkpt lon="'+str(df1.iloc[x][6])+'" lat="'+str(df1.iloc[x][7])+'">\n')
                                            f.writelines('        <ele>58.20000076293945</ele>\n')
                                            #f.writelines('        <time>2014-03-08T07:27:47.000Z</time>')
                                            f.writelines('        <time>'+(dt.datetime((2000+int(str(df1.index[0])[:2])+k),1,1,0,0)+dt.timedelta(df1.iloc[x][5])).strftime('%Y-%m-%dT%H:%M:%S')+'.000Z</time>\n')
                                            f.writelines('      </trkpt>\n')
                                    f.writelines('    </trkseg>\n')
                                    f.writelines('  </trk>\n')
                                    f.writelines('</gpx>\n')
                                    f.close()

    
    # add office layer and set starttime and end time on slider insuring that no drifter appears by looking at 0.05 days prior to start
    if timestart==[]:
	    continue
    timestart=min(timestart)-dt.timedelta(0.05)
    timeend=max(timeend)+dt.timedelta(0.05)
    data.append(str(office_name)+csv[:-4]+'.gpx')  #add our favorite office
    f=open(str(office_name)+csv[:-4]+'.gpx','w')
    
    f.writelines("<?xml version='1.0' encoding='UTF-8'?>\n")
    f.writelines("<gpx version='1.1' creator='drifter'\n")
    f.writelines("  xsi:schemaLocation='http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd http://www.garmin.com/xmlschemas/GpxExtensions/v3 http://www.garmin.com/xmlschemas/GpxExtensionsv3.xsd http://www.garmin.com/xmlschemas/TrackPointExtension/v1 http://www.garmin.com/xmlschemas/TrackPointExtensionv1.xsd'\n")
    f.writelines("  xmlns='http://www.topografix.com/GPX/1/1'\n")
    f.writelines("  xmlns:gpxtpx='http://www.garmin.com/xmlschemas/TrackPointExtension/v1'\n")
    f.writelines("  xmlns:gpxx='http://www.garmin.com/xmlschemas/GpxExtensions/v3' xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance'>\n")
    f.writelines("  <metadata>\n")
    f.writelines("    <link href='connect.garmin.com'>\n")
    f.writelines("      <text>drifter  data</text>\n")
    f.writelines("    </link>\n")
    f.writelines("    <time>2015-03-08T07:27:47.000Z</time>\n")
    f.writelines("  </metadata>\n")
    f.writelines("  <trk>\n")
    f.writelines("    <name>Xavier track</name>\n")
    f.writelines("    <trkseg>\n")
    
    f.writelines('      <trkpt lon="'+str(office_lon)+'" lat="'+str(office_lat)+'">\n')
    f.writelines('        <ele>58.20000076293945</ele>\n')
    #f.writelines('        <time>2014-03-08T07:27:47.000Z</time>')
    f.writelines('        <time>'+timestart.strftime('%Y-%m-%dT%H:%M:%S')+'.000Z</time>\n')
    f.writelines('      </trkpt>\n')
    f.writelines('      <trkpt lon="'+str(office_lon)+'" lat="'+str(office_lat)+'">\n')
    f.writelines('        <ele>58.20000076293945</ele>\n')
    #f.writelines('        <time>2014-03-08T07:27:47.000Z</time>')
    f.writelines('        <time>'+timeend.strftime('%Y-%m-%dT%H:%M:%S')+'.000Z</time>\n')
    f.writelines('      </trkpt>\n')
    
    f.writelines('    </trkseg>\n')
    f.writelines('  </trk>\n')
    f.writelines('</gpx>\n')
    f.close()    
    
    #######################################  Generate Js file to set up leaflet map   #################################################
    
    
    def popupdrif(popup,starttime):
        if float(popup[2])>1.01:
                return '    Drougued drifter  <br> School/Lab :<br> '+popup[1][:popup[1].find('(')]+'<br> Teacher/PI : '+popup[3]+'<br> Deployment_ ID : '+popup[4]+'<br> ESN :'+popup[5]+'<br> Depth : '+popup[2]+'m <br> starts at '+starttime
        else:
                return '    Surface drifter   <br> School/Lab :<br> '+popup[1][:popup[1].find('(')]+'<br> Teacher/PI : '+popup[3]+'<br> Deployment_ ID : '+popup[4]+'<br> ESN :'+popup[5]+'<br> starts at '+starttime
    def popupstart(popup,starttime):
        if float(popup[2])>1.01:
                return '    Drougued drifter Deployed here   <br> School/Lab :<br> '+popup[1][:popup[1].find('(')]+'<br> Teacher/PI : '+popup[3]+'<br> Deployment_ ID : '+popup[4]+'<br> ESN :'+popup[5]+'<br> Depth : '+popup[2]+'m <br> starts at '+starttime
        else:
                return '    Surface drifter Deployed here  <br> School/Lab :<br> '+popup[1][:popup[1].find('(')]+'<br> Teacher/PI : '+popup[3]+'<br> Deployment_ ID : '+popup[4]+'<br> ESN :'+popup[5]  +'<br> starts at '+starttime  
    
    filename=csv[:-4]+'.js'
    f=open(str(filename),'w')
    hexcolor=['#FFFFFF','#FF0000','#808080','#000000','#800000','#FFFF00','#808000','#00FF00','#008000','#008080','#0000FF','#000080','#FF00FF','#800080','#C0C0C0',]
        
    #data=glob.glob('*.gpx')
    data.sort()
    data.reverse() # puts office at top of the list because the underscore had it at the bottom
    
    #data.remove('office.gpx')
    f.write('''var startDate = new Date();
    startDate.setUTCHours(0, 0, 0, 0);
    
    var map = L.map('map', {
        zoom: 12,
        fullscreenControl: true,
        center: [42, -69]
    });
    
    // start of TimeDimension manual instantiation
    var timeDimension = new L.TimeDimension({
            period: "PT5M",
        });
    // helper to share the timeDimension object between all layers
    map.timeDimension = timeDimension; 
    // otherwise you have to set the 'timeDimension' option on all layers.
    
    var player        = new L.TimeDimension.Player({
        transitionTime: 1, 
        loop: true,
        startOver:true
    }, timeDimension);
    
    var timeDimensionControlOptions = {
        player:        player,
        timeDimension: timeDimension,
        position:      'bottomleft',
        autoPlay:      true,
        minSpeed:      1,
        speedStep:     1,
        maxSpeed:      100,
        timeSteps:     20,
        timeSliderDragUpdate: true
    };
    
    var timeDimensionControl = new L.Control.TimeDimension(timeDimensionControlOptions);
    map.addControl(timeDimensionControl);
    
    
    L.control.coordinates({
        position: "bottomright",
        decimals: 3,
        labelTemplateLat: "Latitude: {y}",
        labelTemplateLng: "Longitude: {x}",
        useDMS: true,
        enableUserInput: false
    }).addTo(map);
    
    ''')
    not_drift_index=[]
    #print data
    for i in range(len(data)): #for each drifter
        latlon=[linecache.getline(data[i], 16).split('"')[3],linecache.getline(data[i], 16).split('"')[1]]
        starttime=linecache.getline(data[i], 18)[14:-16]
        if i==0:
    
    
            f.write('''
    var icon'''+data[i][0:-4]+''' = new L.icon({
        iconUrl: 'img/noaa-transparent-logo.png',
        iconSize: [25, 25],
        
    });   
    var customPopup = "<h2>Welcome to our office</h2><h3>Jim Manning <br>508-566-4080 <br>15 Carlson Lane, Falmouth,MA, 02540</h3><br/><img src='https://drive.google.com/uc?id=0Bw4-TSxorJaSOW5aeTl1NXV0czA' alt='maptime logo gif' width='250' height='190'/>";     
    L.marker(['''+str(latlon[0])+''','''+ str(latlon[1])+'''], {icon: icon'''+data[i][0:-4]+'''}).bindPopup(customPopup).addTo(map);   
    var myStyle'''+data[i][0:-4]+''' = {
        "color": "'''+hexcolor[i%len(hexcolor)]+'''",
        "weight": 2,
        "opacity": 0.65
    };
    var geojsonMarkerOptions'''+data[i][0:-4]+''' = {
        radius: 5,
        fillColor: "'''+hexcolor[i%len(hexcolor)]+'''",
        color: "black",
        weight: 1,
        opacity: 0.7,
        fillOpacity: 0.8
    };
    var customLayer'''+data[i][0:-4]+''' = L.geoJson(null,{
        
        style: myStyle'''+data[i][0:-4]+''',
        
        
        pointToLayer: function ( feature,latLng) {
            
     
            return L.circleMarker(latLng,geojsonMarkerOptions'''+data[i][0:-4]+''');
        },
         onEachFeature: function (feature,layer) {
            layer.bindPopup('this is drifter '''+data[i][0:-4]+'''<br> start at '''+starttime+'''')
        }});
    var gpxLayer'''+data[i][0:-4]+''' = omnivore.gpx('data/'''+data[i]+'''', null, customLayer'''+data[i][0:-4]+''').on('ready', function() {});
    
    
    var gpxTimeLayer'''+data[i][0:-4]+''' = L.timeDimension.layer.geoJson(gpxLayer'''+data[i][0:-4]+''', {
        updateTimeDimension: true,
        addlastPoint: true,
        waitForReady: true, 
        });
    
    $('#dtp_start').datetimepicker({
        inline: true,
        value: new Date("'''+starttime[:10]+'''"),
        format: "c"
    });
    $('#dtp_end').datetimepicker({
        inline: true,
        value: new Date("'''+dt.datetime.now().strftime("%Y-%m-%d")+'''"),
        format: "c"
    });
        ''')
        elif float(linecache.getline(data[i],3).split("'")[1].split(',')[2])>0.3:
            popup=linecache.getline(data[i],3).split("'")[1].split(',')
            
            
            f.write('''
    var icon'''+data[i][0:-4]+''' = new L.icon({
        iconUrl: 'img/starticon.png',
        iconSize: [20, 15],
    
    });        
    var marker'''+data[i][0:-4]+'''=L.marker(['''+str(latlon[0])+''','''+ str(latlon[1])+'''], {icon: icon'''+data[i][0:-4]+'''}).bindPopup("'''+popupstart(popup,starttime)+'''");   
    var myStyle'''+data[i][0:-4]+''' = {
        "color": "'''+hexcolor[i%len(hexcolor)]+'''",
        "weight": 6, 
        "opacity": 0.65
    };
    var geojsonMarkerOptions'''+data[i][0:-4]+''' = {
        radius: 5,
        fillColor: "'''+hexcolor[i%len(hexcolor)]+'''",
        color: "black",
        weight: 1,
        opacity: 0.7,
        fillOpacity: 0.8
    };
    var customLayer'''+data[i][0:-4]+''' = L.geoJson(null,{
        
        style: myStyle'''+data[i][0:-4]+''',
        
        
        pointToLayer: function ( feature,latLng) {
            
     
            return L.circleMarker(latLng,geojsonMarkerOptions'''+data[i][0:-4]+''');
        },
         onEachFeature: function (feature,layer) {
            layer.bindPopup("'''+popupdrif(popup,starttime)+'''")
        }});
    var gpxLayer'''+data[i][0:-4]+''' = omnivore.gpx('data/'''+data[i]+'''', null, customLayer'''+data[i][0:-4]+''').on('ready', function() {
        map.fitBounds(gpxLayer'''+data[i][0:-4]+'''.getBounds(), {
            paddingBottomRight: [30, 40]
        });
    });
    
    var gpxTimeLayer'''+data[i][0:-4]+''' = L.timeDimension.layer.geoJson(gpxLayer'''+data[i][0:-4]+''', {
        
        addlastPoint: true,
        waitForReady: true, 
        });
    var gpxaddmarker'''+data[i][0:-4]+''' =L.layerGroup([marker'''+data[i][0:-4]+''',gpxTimeLayer'''+data[i][0:-4]+''']);   
        
        ''')    
        else:
            not_drift_index.append(i)
    not_drift_index.reverse()
    [data.remove(data[q]) for q in  not_drift_index]     
    # now write the legend
    f.write(
    '''
    var officelegend = L.control({
        position: 'bottomright'
    });
    officelegend.onAdd = function(map) {
        var div = L.DomUtil.create('div', 'info legend');
        div.innerHTML += '<img src="img/starticon.png" width="20" height="20"  /> Drifter start location <br> <img src="img/noaa-transparent-logo.png" width="20" height="20"  /> Our Office';
        return div;
    };
    officelegend.addTo(map);
    L.Control.Layers.SelectAll = L.Control.Layers.extend({
        _update: function(){
            L.Control.Layers.prototype._update.apply(this);
            this._addSelectAll();
            return this;
        },
    
        _addSelectAll: function(){
            var button = document.createElement('button');        
            button.className = 'leaflet-control-layers-selector';
            button.innerHTML = 'Select All';
            
    
            L.DomEvent
                .addListener(button, 'click', L.DomEvent.stopPropagation)
                .addListener(button, 'click', L.DomEvent.preventDefault)
                .addListener(button, 'click', this._onSelectAllClick, this);
            this._overlaysList.insertBefore(button, this._overlaysList.firstChild);
            return button;
        },
    
        _onSelectAllClick: function(){
            // copied from _onInputClick
            var i, input, obj,
                inputs = this._form.getElementsByTagName('input'),
                inputsLen = inputs.length;
    
            this._handlingClick = true;
    
            for (i = 3; i < inputsLen; i++) {
                input = inputs[i];
                obj = this._layers[input.layerId];
    
                if (obj.overlay && !input.checked) {
                    this._map.addLayer(obj.layer);
                    //this._map.removeLayer(obj.layer);
                    input.checked = true;
                }
                
                else {
                    //this._map.addLayer(obj.layer);
                    this._map.removeLayer(obj.layer);
                    input.checked = false;
                }
            }
    
            this._handlingClick = false;
    
            this._refocusOnMap();        
        },
    
    });
    ''')
    # now write  layers including base layers
    f.writelines('\nvar overlayMaps = {\n')
    for i in range(len(data)):
        if i!=0:
    
                f.write(
    '''\n"'''+data[i][0:-4]+'''": gpxaddmarker'''+data[i][0:-4]+''',''')
    f.write(
    '''};
    
    var baseLayers = getCommonBaseLayers(map); // see baselayers.js
    L.control.layers.selectAll = function(baseLayers, overlays, options) {
        return new L.Control.Layers.SelectAll(baseLayers, overlays, options);
    };
    L.control.layers.selectAll(baseLayers, overlayMaps).addTo(map);''')
      
    for i in range(len(data)):
        if data[i]==str(office_name)+csv[:-4]+'.gpx':
                f.write(
    '''\ngpxTimeLayer'''+data[i][0:-4]+'''.addTo(map);''')
        else:    
                f.write(
    '''\ngpxaddmarker'''+data[i][0:-4]+'''.addTo(map);''')
    
    # add time label w/calender
    f.write('''
    $("#btn_timerange").click(function(){
        var startTime = new Date($('#dtp_start').val());
        var endTime = new Date($('#dtp_end').val());
        var newAvailableTimes = L.TimeDimension.Util.explodeTimeRange(startTime, endTime, 'PT1H');
        map.timeDimension.setAvailableTimes(newAvailableTimes, 'replace');
        map.timeDimension.setCurrentTime(startTime);
    });
    
    $("#btn_limitrange").click(function(){
        var startTime = new Date($('#dtp_start').val());
        var endTime = new Date($('#dtp_end').val());    
        map.timeDimension.setLowerLimit(startTime);
        map.timeDimension.setUpperLimit(endTime);
        map.timeDimension.setCurrentTime(startTime);
    });
    ''')
    f.close()
    
#############################################  Create html for each group  ######################
    filename_html=csv[:-4]+'.html'
    f2=open(str(filename_html),'w')
    f2.write('''
    <!DOCTYPE html>
    <html>
        <head>
            <title>NOAA drifter track</title>
            <meta charset="utf-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
    
            <link rel="stylesheet" href="http://cdnjs.cloudflare.com/ajax/libs/highlight.js/8.4/styles/default.min.css">
            <link rel="stylesheet" href="js/vendors/leaflet-0.7.7/leaflet.css" />
            <link rel="stylesheet" href="js/vendors/leaflet-plugins/Leaflet.Coordinates-0.1.3.css" />
            <link rel="stylesheet" href="js/vendors/leaflet-plugins/Control.FullScreen.css" />
            <link rel="stylesheet" href="http://ajax.googleapis.com/ajax/libs/jqueryui/1.11.0/themes/smoothness/jquery-ui.css" />
            <link rel="stylesheet" href="../src/leaflet.timedimension.control.css" />
            <link rel="stylesheet" href="css/style.css" />
            <link rel="stylesheet" href="js/vendors/jquery.datetimepicker.css" />
        </head>
        <body>
            <div class="container">
                <div id="header">
                    <h1><center>Drifter tracks</center>  </h1> 
                </div>
                <div id="map" class="map" ></div>
                <p>
                    <h2>Select start time and end time of the animation loop</h2>
                    <div style="float:left; margin-right: 10px;">
                    <label for="start_time">Start time (GMT)</label><br/><input id="dtp_start" name="start_time" type="text" >
                    </div>
                    <div style="float:left; margin-right: 10px;">
                    <label for="end_time">End time (GMT)</label><br/><input id="dtp_end" name="end_time" type="text" >                
                    </div>
                    <div style="float:left; padding-top: 50px;">
                        <button type="button" id="btn_limitrange" class="btn" >Apply new time limits range</button><br />
                        <p>Click button above when you set drifter time range  </p>
                        
                        <button type="button" id="btn_timerange" class="btn" >Apply time to available range</button>
                        <p>Click second button while you need to reset time slider <br>after you set time range</p> 
                        
                    </div>
                </p>
                <div style="clear: both;"></div>
           
    
    
                
                <pre><code class="javascript" id="code"></code></pre>
                <div class="disclaimer">
                    <center>Reference <a href="http://apps.socib.es/Leaflet.TimeDimension/examples/" title="Timedimension">Timedimension</a> from <a href="http://apps.socib.es/Leaflet.TimeDimension/examples/" title="timedimension">http://apps.socib.es/Leaflet.TimeDimension/examples/</a> is licensed under <a href="https://github.com/socib/Leaflet.TimeDimension/blob/master/LICENSE" title="2014 ICTS SOCIB">2014 ICTS SOCIB</a><br>Presented py <a>Jim Manning, Xavier Xu (NOAA NEFSC)  &nbsp&nbsp Email: james.manning@noaa.gov ; xhx509@gmail.com </a> </center>    
                                       
            </div>
    
            <script type="text/javascript" src="js/vendors/jquery-2.0.0.min.js"></script>
            <script type="text/javascript" src="js/vendors/jquery-ui-1.10.2.min.js"></script>
    
            <script type="text/javascript" src="js/vendors/leaflet-0.7.7/leaflet.js"></script>
            <script type="text/javascript" src="js/vendors/leaflet-plugins/Leaflet.Coordinates-0.1.3.min.js"></script>
            <script type="text/javascript" src="js/vendors/leaflet-plugins/Control.FullScreen.js"></script>
            <script type="text/javascript" src="js/vendors/leaflet-plugins/leaflet-omnivore.js"></script>
            <script type="text/javascript" src="js/vendors/iso8601.js"></script>
    
            <script type="text/javascript" src="../src/leaflet.timedimension.js"></script>
            <script type="text/javascript" src="../src/leaflet.timedimension.util.js"></script>
            <script type="text/javascript" src="../src/leaflet.timedimension.layer.js"></script>
            <script type="text/javascript" src="../src/leaflet.timedimension.layer.wms.js"></script>
            <script type="text/javascript" src="../src/leaflet.timedimension.layer.geojson.js"></script>
            <script type="text/javascript" src="../src/leaflet.timedimension.player.js"></script>
            <script type="text/javascript" src="../src/leaflet.timedimension.control.js"></script>
            <script type="text/javascript" src="js/baselayers.js"></script>
            <script type="text/javascript" src="js/vendors/DateFormat.js"></script>
            <script type="text/javascript" src="js/vendors/iso8601.js"></script>
    
            <script type="text/javascript" src="js/vendors/leaflet-plugins/NonTiledLayer.js"></script>
            <script type="text/javascript" src="js/vendors/leaflet-plugins/NonTiledLayer.WMS.js"></script>
            <script type="text/javascript" src="js/vendors/jquery.datetimepicker.full.min.js"></script>
    
            <script type="text/javascript" src="data/'''+filename+'''"></script>
            <script src="http://cdnjs.cloudflare.com/ajax/libs/highlight.js/8.4/highlight.min.js"></script>
    
    
        </body>
    </html>
    ''')
    f2.close()
#############################################  upload both Js file,html and Gpx files to /anon_ftp/data  ##############################################################

htmlfiles=glob.glob('*.html')
jsfiles=glob.glob('*.js')
gpxfiles=glob.glob('*.gpx') #put js file in data folder
gpxfiles.extend(jsfiles)
gpxfiles.extend(htmlfiles)
for u in gpxfiles:
            #print u
            session = ftplib.FTP('216.9.9.126','huanxin','123321')
            file = open(u,'rb') 
            session.cwd("/data")  
            #session.retrlines('LIST')               # file to send
            session.storlines("STOR "+u , open(u, 'r'))   # send the file
            #session.close()
            session.quit()# close file and FTP
            file.close() 
            os.remove(u)
            time.sleep(2)
