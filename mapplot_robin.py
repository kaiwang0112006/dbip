import matplotlib as mpl
mpl.use('Agg')
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import pandas as pd
import time
from matplotlib.colors import *
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.colors as mcolors

df = pd.read_csv('testcut.csv')
dfgp = df.groupby(['latitude','longitude'],as_index=False).agg(['count']).reset_index()

dfgp['count'] = dfgp[('city','count')]
  
# make sure the value of resolution is a lowercase L,
#  for 'low', not a numeral 1
plt.figure(figsize=(16,12))
plt.title("Map of the Internet")
ax = plt.gca()
my_map = Basemap(projection='robin', resolution = 'l', area_thresh = 1000.0,lat_0=0, lon_0=10)
 
#my_map.drawcoastlines()
my_map.drawcountries(color='white')
my_map.fillcontinents(color='black',lake_color='black')
my_map.drawcoastlines(linewidth=0.1,color='white')
my_map.drawmapboundary(fill_color='black')
 
my_map.drawmeridians(np.arange(0, 360, 30))
my_map.drawparallels(np.arange(-90, 90, 30))


#norm = mpl.colors.Normalize(vmin=min(dfgp['count']), vmax=max(dfgp['count']))
{'jet','autumn','gnuplot','YlOrRd','rainbow'}
ocmap = plt.get_cmap('gist_rainbow_r')
def truncate_colormap(cmap, minval=0.0, maxval=1.0, n=100):
    new_cmap = LinearSegmentedColormap.from_list(
        'trunc({n},{a:.2f},{b:.2f})'.format(n=cmap.name, a=minval, b=maxval),
        cmap(np.linspace(minval, maxval, n)))
    return new_cmap

cmap = truncate_colormap(ocmap, 0.5,1)

for i in range(len(dfgp)):
    if dfgp.iloc[i]['latitude'][0] != 'None' and dfgp.iloc[i]['longitude'][0] != 'None':
        x, y = my_map(float(dfgp.iloc[i]['longitude'][0]),  float(dfgp.iloc[i]['latitude'][0]))

        my_map.plot(x, y, marker='o',color=cmap(dfgp.iloc[i]['count'][0].astype(np.int32)),markersize=2)   

im = ax.imshow([dfgp['count']], cmap=cmap)

divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="1%", pad=0.05)

plt.colorbar(im, cax=cax)

plt.savefig('map_robin.png')
