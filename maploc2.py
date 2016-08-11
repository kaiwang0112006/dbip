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
    
def do_geocode(country,state,city):
    try:
        return findLoc(country,state,city)
    except:
        time.sleep(5)
        return do_geocode(country,state,city)


fout = open('iploc.csv','w')
fout.write("country,state,city,latitude,longitude\n")
with open('dbip-city-2016-08.csv') as fin:
    spamreader = csv.reader(fin, delimiter=',', quotechar='"')
    for row in spamreader:
        loc = do_geocode(row[2],row[3],row[4])
    time.sleep(2)
    latitude = loc[0]
    longitude = loc[1]
    try:
        fout.write("%s,%s,%s,%s,%s\n" % (row[2],row[3],row[4],latitude,longitude))
    except:
        fout.write("%s,%s,%s,%s,%s\n" % (row[2],row[3],row[4],'none','none'))
fout.close()
