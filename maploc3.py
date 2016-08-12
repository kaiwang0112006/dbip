import pandas as pd
from geopy.geocoders import Nominatim
import time
import csv

def findLoc(country,state,city):
    query=','.join([country,state,city])
    geolocator = Nominatim()
    location = geolocator.geocode(query,timeout=None)
    try:
        return (location.latitude, location.longitude)
    except:
        return ('None','None')
    
def do_geocode(country,state,city,recursion=0):
    try:
        return findLoc(country,state,city)
    except:
        if recursion > 150:
            return ('None','None')
        time.sleep(5)
        return do_geocode(country,state,city,recursion=recursion + 1)

citys = {}
fout = open('iploc2.csv','w')
fout.write("country,state,city,latitude,longitude\n")
print "reading existed"
with open('iploc.csv') as fin:
    spamreader = csv.reader(fin, delimiter=',', quotechar='"')
    for eachline in spamreader:
        citys[(eachline[0],eachline[1],eachline[2])] = (eachline[3],eachline[4])

print "reading all..."
with open('dbip-city-2016-08.csv') as fin:
    spamreader = csv.reader(fin, delimiter=',', quotechar='"')
    for row in spamreader:
        if (row[2],row[3],row[4]) not in citys:
            #print row
            loc = do_geocode(row[2],row[3],row[4])
            time.sleep(2)
            latitude = loc[0]
            longitude = loc[1]
            citys[(row[2],row[3],row[4])] = (latitude,longitude)
        else:
            latitude = citys[(row[2],row[3],row[4])][0]
            longitude = citys[(row[2],row[3],row[4])][1]
        try:
            fout.write("\"%s\",\"%s\",\"%s\",\"%s\",\"%s\"\n" % (row[2],row[3],row[4],latitude,longitude))
        except:
            fout.write("\"%s\",\"%s\",\"%s\",\"%s\",\"%s\"\n" % (row[2],row[3],row[4],'None','None'))
fout.close()
print 'done'
