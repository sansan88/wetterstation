opendata.py
from StringIO import StringIO
from zipfile import ZipFile
from urllib import urlopen
import json
import re
import string
import time


while True:

 print "open url"
 url = urlopen("http://data.geo.admin.ch.s3.amazonaws.com/ch.meteoschweiz.swissmetnet/data.zip")

 print "open zip file"
 zipfile = ZipFile(StringIO(url.read()))

#iterator
 i = 0
 index = 0

#json "file"
 output = []

#Open File
 f = open('wetterstation/wetterdaten_schweiz.json','w')

#Loop file
 for line in zipfile.open('VQHA69.txt').readlines():

     if i == 0:
        #header MeteoSchweiz / MeteoSuisse / MeteoSvizzera / MeteoSwiss
         header = line
         print header
     if i == 2:
#stn|time|tre200s0|sre000z0|rre150z0|dkl010z0|fu3010z0|pp0qnhs0|fu3010z1|ure200s0|prestas0|pp0qf
        ueberschrift = line.split('|')
        print ueberschrift
     if i > 3: #DATA
         data = line.split('|')
         d = {}

         for index, item in enumerate(data):
             key = ueberschrift[index]
             value = item

             key.rstrip()
             key.replace('\\', "")

             value.rstrip()
             value.replace('\\', "")

             print key + "/" + value
             d[key]=value

         output.append(d)

            #print json.dumps(line.split('|'))
#            print line.split('|')

     i += 1
#save to mongo db...
# f = open('wetterstation/wetterdaten_schweiz.json','w')

#print json.dumps(output, separators=(',',':'))

 f.write(json.dumps(output, ensure_ascii=False, encoding="utf-8"))
# f.write(json.dumps(output, separators=(',',':')))

 f.close()
 time.sleep(600)
