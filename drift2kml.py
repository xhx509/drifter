#################################################################################################
# The intended purpose of this program is to download raw .dat file containing drifter tracks,
# then create a kml file from that data.  Written to use Python 2.6.5.
#
# Initial version 3-JANUARY-2011
# Written by Tanya Stoyanova
# modified by huanxin 2014
# The year is hardcoded 2014 ,So please modify it to what you want
#   u=open(filename)
#   u=urllib2.urlopen('http://www.nefsc.noaa.gov/drifter/'  + filename)
    # bring the file into python and change it's extension to '.csv'
#Please modify choose part above ,then you can get data from website or local file
#
###################################################################################################


import csv
import urllib2
import sys

## Name of input file
#filename=sys.argv[1]
filename='drift_X.dat'
u=urllib2.urlopen('http://www.nefsc.noaa.gov/drifter/'  + filename)
#filename='drift_ep_2014_31.dat'
#Name of output file
out_file = filename[0:-4] + ".kml"
ids=[]
verts=[]
vertid=[]

## KML header
header = "<?xml version=\"1.0\" encoding=\"UTF-8\"?><kml xmln=\"http://www.opengis.net/kml/2.2\">\n<Document>\n"
## KML body

body = ""

## KML footer
footer = ("</Document>\n</kml>\n")

#u=open(filename)
#u=urllib2.urlopen('http://www.nefsc.noaa.gov/drifter/'  + filename)
    # bring the file into python and change it's extension to '.csv'
localfile = open ('filename', 'w')
    # write the file to the local computer
localfile.write(u.read())
    # close IO stream and web connecion
localfile.close()
    # import the .csv file into Python space
csv.register_dialect('spacedelimitedfixedwidth', delimiter=' ',skipinitialspace=True, quoting=csv.QUOTE_NONE)    
with open('filename','rb') as f:
    dataReader = csv.reader(f,'spacedelimitedfixedwidth')
    dataReader.next()
    try:
        for row in dataReader:
            verts.append(row)
    except csv.Error, e:
        sys.exit()#('file %s, line %d: %s' % (filename, reader.line_num, e))

#for row in dataReader:
    #verts.append(row)

# Current year
year = "2015"
#color for lines
#color=('b','g','r','k','w','y')
color=('ff0000ff','ffffffff','ffff0000','ff330066','ff33ffff','ffccff33','ff660099','ffff0099','ff33ccff','ffcc6699',
       'ff0000ff','ffffffff','ffff0000','ff330066','ff33ffff','ffccff33','ff660099','ffff0099','ff33ccff','ffcc6699',
       'ff0000ff','ffffffff','ffff0000','ff330066','ff33ffff','ffccff33','ff660099','ffff0099','ff33ccff','ffcc6699',
       'ff0000ff','ffffffff','ffff0000','ff330066','ff33ffff','ffccff33','ff660099','ffff0099','ff33ccff','ffcc6699',
       'ff0000ff','ffffffff','ffff0000','ff330066','ff33ffff','ffccff33','ff660099','ffff0099','ff33ccff','ffcc6699',
       'ff0000ff','ffffffff','ffff0000','ff330066','ff33ffff','ffccff33','ff660099','ffff0099','ff33ccff','ffcc6699',
       'ff0000ff','ffffffff','ffff0000','ff330066','ff33ffff','ffccff33','ff660099','ffff0099','ff33ccff','ffcc6699',
       'ff0000ff','ffffffff','ffff0000','ff330066','ff33ffff','ffccff33','ff660099','ffff0099','ff33ccff','ffcc6699',
       'ff0000ff','ffffffff','ffff0000','ff330066','ff33ffff','ffccff33','ff660099','ffff0099','ff33ccff','ffcc6699',
       'ff0000ff','ffffffff','ffff0000','ff330066','ff33ffff','ffccff33','ff660099','ffff0099','ff33ccff','ffcc6699',
       'ff0000ff','ffffffff','ffff0000','ff330066','ff33ffff','ffccff33','ff660099','ffff0099','ff33ccff','ffcc6699',
       'ff0000ff','ffffffff','ffff0000','ff330066','ff33ffff','ffccff33','ff660099','ffff0099','ff33ccff','ffcc6699',
       'ff0000ff','ffffffff','ffff0000','ff330066','ff33ffff','ffccff33','ff660099','ffff0099','ff33ccff','ffcc6699',
       'ff0000ff','ffffffff','ffff0000','ff330066','ff33ffff','ffccff33','ff660099','ffff0099','ff33ccff','ffcc6699',
       'ff0000ff','ffffffff','ffff0000','ff330066','ff33ffff','ffccff33','ff660099','ffff0099','ff33ccff','ffcc6699',
       'ff0000ff','ffffffff','ffff0000','ff330066','ff33ffff','ffccff33','ff660099','ffff0099','ff33ccff','ffcc6699','','','','','','','','','','','','','','','',)
#color=('#FF0000', 'ffffffff', 'ffff0000', '#660033', '#FFFF33', '#33FFCC', '#990066', '#9900FF', '#FFCC33', '#9966CC', '#33FFFF', '#FF00CC', '#FF0000', '#99CC66', '#3333CC', '#FF66FF', '#660033', '#FFFF33', '#33FFCC', '#990066', '#9900FF', '#FFCC33', '#9966CC', '#33FFFF', '#FF00CC', '#2e8b57', '#f5f5f5', '#fa8072', '#008080', '#9acd32', '#800080', '#dda0dd', '#ffa500', '#000080', '#48d1cc', '#ff00ff', '#2e8b57', '#f5f5f5', '#fa8072', '#008080', '#FF0000', '#99CC66', '#3333CC', '#FF66FF', '#660033', '#FFFF33', '#33FFCC', '#990066', '#9900FF', '#FFCC33', '#9966CC', '#33FFFF', '#FF00CC', '#FF0000', '#99CC66', '#3333CC', '#FF66FF', '#660033', '#FFFF33', '#33FFCC', '#990066', '#9900FF', '#FFCC33', '#9966CC', '#33FFFF', '#FF00CC', '#2e8b57', '#f5f5f5', '#fa8072', '#008080', '#9acd32', '#800080', '#dda0dd', '#ffa500', '#000080', '#48d1cc', '#ff00ff', '#2e8b57', '#f5f5f5', '#fa8072', '#008080', '#FF0000', '#99CC66', '#3333CC', '#FF66FF', '#660033', '#FFFF33', '#33FFCC', '#990066', '#9900FF', '#FFCC33', '#9966CC', '#33FFFF', '#FF00CC', '#2e8b57', '#99CC66', '#f5f5f5', '#fa8072', '#008080', '#9acd32', '#800080', '#dda0dd', '#ffa500', '#000080', '#48d1cc', '#ff00ff', '#2e8b57', '#f5f5f5', '#fa8072', '#FF0000', '#f5f5f5', '#FF66FF', '#660033', '#FFFF33', '#33FFCC', '#990066', '#9900FF', '#FFCC33', '#9966CC', '#33FFFF', '#FF00CC', '#FF0000', '#99CC66', '#3333CC', '#FF66FF', '#660033', '#FFFF33', '#33FFCC', '#990066', '#9900FF', '#FFCC33', '#9966CC', '#33FFFF', '#FF00CC', '#2e8b57', '#f5f5f5', '#fa8072', '#008080', '#9acd32', '#800080', '#dda0dd', '#ffa500', '#000080', '#48d1cc', '#ff00ff', '#2e8b57', '#f5f5f5', '#fa8072', '#008080', '#FF0000', '#99CC66', '#3333CC', '#FF66FF', '#660033', '#FFFF33', '#33FFCC', '#990066', '#9900FF', '#FFCC33', '#9966CC', '#33FFFF', '#FF00CC', '#FF0000', '#99CC66', '#3333CC', '#FF66FF', '#660033', '#FFFF33', '#33FFCC', '#990066', '#9900FF', '#FFCC33', '#9966CC', '#33FFFF', '#FF00CC', '#2e8b57', '#f5f5f5', '#fa8072', '#008080', '#9acd32', '#800080', '#dda0dd', '#ffa500', '#000080', '#48d1cc', '#ff00ff', '#2e8b57', '#f5f5f5', '#fa8072', '#008080', '#FF0000', '#99CC66', '#3333CC', '#FF66FF', '#660033', '#FFFF33', '#33FFCC', '#990066', '#9900FF', '#FFCC33', '#9966CC', '#33FFFF', '#FF00CC', '#2e8b57', '#99CC66', '#f5f5f5', '#fa8072', '#008080', '#9acd32', '#800080', '#dda0dd', '#ffa500', '#000080', '#48d1cc', '#ff00ff', '#2e8b57', '#f5f5f5', '#fa8072')
#color=('64FFFFFF','641400FF','6414F0FF','6414F000','64F0FF14','641478FF','6414B4FF','6478FFF0','6400783C','64000000','6478AAF0','','','','','',)
#color=('64FFFFFF', '641400FF', '6414F000', '6414F0FF', '647800F0', '23E678B4','508C783C','501E7878','5078FFF0','23000000', '23FFFFFF', '2314F000', '231400FF', '2378003C', '23783CF0', '23E678B4','508C783C','501E7878','5078FFF0')
#href for icons
href=('http://maps.google.com/mapfiles/kml/shapes/sailing.png','http://maps.google.com/mapfiles/kml/pal4/icon49.png','http://maps.google.com/mapfiles/kml/pal3/icon49.png','http://www.nefsc.noaa.gov/epd/ocean/MainPage/drift/shaded_dot.png','http://www.nefsc.noaa.gov/epd/ocean/MainPage/drift/shaded_dot.png')
ids = []
for vert in verts:
    ids.append(vert[0])
ids = list(set(ids))
for id in ids: print id
k=2
coords=""
for id in ids:

    for vert in verts:
      
        if id==vert[0]:
            longitude = float(vert[7])
            latitude = float(vert[8])
            mo = int(vert[2])
            day = int(vert[3])
            if mo < 10:
                mo = "0" + str(mo)
            if day < 10:
                day = "0" + str(day)
            timestamp = year + "-" + str(mo) + "-" + str(day) + "T" + "12:00:00Z"
            kml_points =("<Placemark>\n"
                "<TimeStamp>"
                "<when>%s</when>"
                "</TimeStamp>\n"
                "<styleUrl>#track_style</styleUrl>\n"
                "<description>%s,%s</description>"
                "<Point><coordinates>%f,%f</coordinates></Point>\n"
                "</Placemark>\n"
                "<Style id=\"track_style\">\n"
                "<IconStyle>\n"
                "<color>%s</color>\n"
                "<scale>0.6</scale>"
                "<Icon>\n"
                "<href>%s</href>\n"
                "</Icon>\n"
                "</IconStyle>\n"
                "</Style>\n")  %(timestamp,id,timestamp,longitude,latitude,color[k],href[0])
            coords += ("%f,%f\n") %(longitude,latitude)
            print timestamp
            body += kml_points 
          
    
    kml_line=("<Placemark>\n"
            "<name>Drifter Path</name>\n"
            "<LineString>\n"
            "<coordinates>%s</coordinates>\n"
            "</LineString>\n"
            "<Style>\n"
            "<LineStyle>\n"
            "<color>%s</color>\n"
            "<width>2</width>\n"
            "</LineStyle>\n"
            "</Style>\n"
            "</Placemark>\n")  %(coords,'#ff0000')
    coords=""
    body += kml_line
    k+=1
  
       
kmlOutput = header + body + footer

## Write file

f = open('/net/nwebserver/drifter/'+out_file, 'w')
f.write (kmlOutput)
f.close()
