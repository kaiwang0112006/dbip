import matplotlib as mpl
mpl.use('Agg')
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import pandas as pd
import time

df = pd.read_csv('iploc2.csv')
dfgp = df.groupby(['latitude','longitude'],as_index=False).agg(['count']).reset_index()

dfgp['count'] = dfgp[('city','count')]
  
# make sure the value of resolution is a lowercase L,
#  for 'low', not a numeral 1
plt.figure(figsize=(26,22),dpi=100)

my_map = Basemap(projection='robin', resolution = 'l', area_thresh = 1000.0,lat_0=0, lon_0=10)
 
#my_map.drawcoastlines()
my_map.drawcountries(color='white')
my_map.fillcontinents(color='black',lake_color='black')
my_map.drawcoastlines(linewidth=0.5,color='white')
my_map.drawmapboundary(fill_color='black')
 
my_map.drawmeridians(np.arange(0, 360, 30))
my_map.drawparallels(np.arange(-90, 90, 30))


norm = mpl.colors.Normalize(vmin=min(dfgp['count']), vmax=max(dfgp['count']))
cmap = plt.get_cmap('hot')

for i in range(len(dfgp)):
    if dfgp.iloc[i]['latitude'][0] != 'None' and dfgp.iloc[i]['longitude'][0] != 'None':
        x, y = my_map(dfgp.iloc[i]['longitude'][0],  dfgp.iloc[i]['latitude'][0])

        my_map.plot(x, y, marker='o',color=cmap(dfgp.iloc[i]['count'][0]),markersize=5)    

plt.title("Map of the Internet") 
plt.savefig('map_robin.png')
