#! /usr/bin/Rscript


########## Import necessary libraries
import numpy as np
from netCDF4 import Dataset
# import glob
# import matplotlib.pyplot as plt
# from matplotlib import gridspec
# from mpl_toolkits.basemap import Basemap
# import datetime
import os
import io
import scipy as sp
### in order to execute R in Python
import subprocess
from os.path import basename
# import pandas as pd
# import csv
from collections.abc import Iterable
import sys

######### Assignemt of netcdf file to a variable
in_file='data/chirps.nc'

#### Reading in the variables of the netcdf data
nc_fil = Dataset(in_file,'r')
# print(nc_fil.variables)
lons= nc_fil.variables['lon'][:]
lats= nc_fil.variables['lat'][:]
prec = nc_fil.variables['precip'][:]

#### Read XY values from bash arguments
xmin = float(sys.argv[1])
xmax = float(sys.argv[3])
ymin = float(sys.argv[4])
ymax = float(sys.argv[2])

#### Create arrays of coords
idx_latarea = np.where((lats >=  ymin ) & (lats <=  ymax))[0]
idx_lonarea = np.where((lons >= xmin) & (lons <= xmax))[0]
la1 = lats[idx_latarea[0]:idx_latarea[-1]+1]
lo1 = lons[idx_lonarea[0]:idx_lonarea[-1]+1]

####### Subset precipitation for selected AOI
prec = prec[:,:,idx_latarea[0]:idx_latarea[-1]+1, idx_lonarea[0]:idx_lonarea[-1]+1]

#### Looping through each grid to produce 560 grid boxes of precipittaion data
rains=[] 
for i in range(len(la1)):
	for j in range(len(lo1)):
		 rains.append(prec[:,:,i,j])
#### "rains"" becomes a list of lists (sublists --> year; DOY; latitude; longitude) and needs to be flattened
# https://stackoverflow.com/questions/952914/how-to-make-a-flat-list-out-of-a-list-of-lists
rs = []
for i in range(len(rains)):
    rs.append([item for sublist in rains[i] for item in sublist])

####### Create the dates (YEAR, DOY)
# Consider that the downloaded data has only year (each file) and a DOY (a band for each day).
# Each year has 365 days... idk why!
yr = []
doy = []
for y in range(1981,2021):
    for d in range(1,366):
        yr.append(y)
        doy.append(d)
        
# Put YEAR and DOY into array
dates = np.array([yr,doy])

###### Saving files ready for R code on various indices
for i in range(len(rains)):
    print('Done with RR_GH_'+str(i+1))
    np.savetxt('All_grids_data/'+'RR_GH_'+str(i+1),np.c_[dates[0],dates[1],rs[i]],fmt='%s')
