import pandas as pd
from geopy.geocoders import Nominatim
import time

def findLoc(country,state,city):
    query=','.join([country[0],state[0],city[0]])
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

fout = open('iplociAll.csv','w')
df = pd.read_csv('dbip-city-2016-08.csv',header=None,names=['ip','mask','country','state','city'])
for i in range(len(df)):
    loc = do_geocode(df.iloc[i]['country'],df.iloc[i]['state'],df.iloc[i]['city'])
    time.sleep(2)
    df.iloc[i]['latitude'] = loc[0]
    df.iloc[i]['longitude'] = loc[1]
    try:
        fout.write("%s,%s,%s,%s,%s\n" % (df.iloc[i]['country'][0],df.iloc[i]['state'][0],df.iloc[i]['city'][0],df.iloc[i]['latitude'],df.iloc[i]['longitude']))
    except:
        fout.write("%s,%s,%s,%s,%s\n" % (df.iloc[i]['country'][0],df.iloc[i]['state'][0],df.iloc[i]['city'][0],'none','none'))
fout.close()

