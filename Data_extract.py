#! /usr/bin/Rscript


########## Import necessary libraries
import numpy as np
from netCDF4 import Dataset
import glob
import matplotlib.pyplot as plt
from matplotlib import gridspec
from mpl_toolkits.basemap import Basemap
import datetime
import os
import io
import scipy as sp
### in order to execute R in Python
import subprocess
from os.path import basename
import pandas as pd
import csv
import subprocess
#import my_lib as ml


#in_file = glob.glob('*.nc')
######### Assignemt of netcdf file to a variable
in_file='chirps.nc'


	
#### Reading in the variables of the netcdf data
nc_fil = Dataset(in_file,'r')
lons= nc_fil.variables['longitude'][:]
lats= nc_fil.variables['latitude'][:]
prec = nc_fil.variables['precip'][:]
#time = nc_fil.variables['T'][:]

#### Figure setting 
fig = plt.figure(figsize=(10,8))



#lon_range=np.arange(-3.5,1.5,0.5)

#lat_range=np.arange(4.5,11.5,0.5)

'''
###command to give long lat ranges
lon_beg = input('Please enter your lowest longitude: ')
lon_end = input('Please enter your highest longitude: ')

lat_beg = input('Please enter your lowest latitude: ')
lat_end = input('Please enter your highest latitude: ')

'''

###indicate spacing of interest for meridians and parallels
#spc = input('Please indicate the grid spacing of your interest: ')

#print('This will only take a second')
	
#m = Basemap(projection='merc',llcrnrlon=lon_beg,llcrnrlat=lat_beg,urcrnrlon=lon_end,urcrnrlat=lat_end,resolution='l')

spc=0.05
lat_beg=0
lat_end=30
lon_beg=-20
lon_end=15

m = Basemap(projection='merc',llcrnrlon=lon_beg,llcrnrlat=lat_beg,urcrnrlon=lon_end,urcrnrlat=lat_end,resolution='l')
m.drawcoastlines()
m.drawstates()
m.drawcountries()
m.drawlsmask(land_color='Linen', ocean_color='#CCFFFF') # can use HTML names or codes for colors
#m.drawcounties()
parallels = np.arange(lat_beg,lat_end,spc) # make latitude lines ever 5 degrees from 30N-50N
meridians = np.arange(lon_beg,lon_end,spc) # make longitude lines every 5 degrees from 95W to 70W
m.drawparallels(parallels,labels=[1,0,0,0],fontsize=5.5)
m.drawmeridians(meridians,labels=[0,0,0,1],fontsize=5.5)

x,y= np.meshgrid(lons,lats)

a,b = m(x,y)

plt.legend(loc='upper center', shadow='True', fontsize='14')

clevs = np.arange(0,6,0.05)


#ppt = m.contourf(a,b,prec[0,:],clevs)

####Selection of an area of interest 


idx_latarea = np.where((lats >=  8.125 ) & (lats <=  11.125))[0]
idx_lonarea = np.where((lons >= -3.875) & (lons <= 1.875))[0]
la1 = lats[idx_latarea[0]:idx_latarea[-1]+1]
lo1 = lons[idx_lonarea[0]:idx_lonarea[-1]+1]

##############precipitation for selected area above

prec = prec[:,idx_latarea[0]:idx_latarea[-1]+1, idx_lonarea[0]:idx_lonarea[-1]+1]

#x,y= np.meshgrid(lo1,la1 )

#a,b = m(x,y)


#ppt = m.contourf(a,b,prec[0,:],clevs)

####selection of a particular grid point
####creating lists to append all precipitaion values from grids
#sizes = (7670, 560)
#list_grids = np.zeros(sizes)


#### Looping through each grid to produce 560 grid boxes of precipittaion data
rains=[] 
for i in range(len(la1)):
	for j in range(len(lo1)):
		 rains.append(prec[1:,i,j])


####Creating the year, month, day data for the file

yr = []
mon = []
day = []


beg = datetime.datetime(1981, 01, 01)
end = datetime.datetime(2020, 12, 31)
t_step = datetime.timedelta(days=1)

###################################################Mke this work

while beg < end:
	
    	yr.append(beg.strftime('%Y'))
	mon.append(beg.strftime('%m'))
	day.append(beg.strftime('%d'))
   	beg += t_step

######## creation of arrays for dates, minT, maxT data
dates = np.array([yr,mon,day]) ####dates in array format
minT  = [-99.9]*len(dates[0]) ###an array of min tempertature
maxT  = [-99.9]*len(dates[0])


 ###an array of max tempertature
	
########### Saving all grid files into the one directory: Not ready for indices yet
################## Next we have to convert all of these special files for indices compartible file format "\r\n"


###### Saving files ready for R code on various indices
for i in range(len(rains)):
	print('Done with RR_GH_'+str(i+1))

	
	np.savetxt('All_grids_data/'+'RR_GH_'+str(i+1),np.c_[dates[0],dates[1],dates[2],rains[i]],fmt='%s')

print('Completed for all grids')


'''
############## Now converting all files into indices compartible file format "\r\n"

path=os.getcwd()


infiles=sorted(glob.glob(os.path.join('All_grids_data/*')))

#out_file=open('2.txt','w')

for filename in infiles:

			
	f_out= open('Indice_com_files/'+basename(filename), 'w')

	with open(filename,'r') as in_file:
		
		for line in in_file:
			lines=line.split()
			ppt = round(float(lines[3]),1)
			#writer = csv.writer(f, delimiter='\t')
 			f_out.write(lines[0]+'\t'+lines[1]+'\t'+lines[2]+'\t'+str(ppt)+'\t'+lines[4]+'\t'+lines[5]+'\r\n')		

	print "Completed with "+ str(filename)



#subprocess.call(["/usr/bin/Rscript", "--vanilla", "rclimdex1.1_131115.r"])

'''
