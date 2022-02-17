#!/usr/bin/env python

# Import the necessary modules:
import glob
import os, math
import sys
import numpy as np
import scipy as sp
import gdal
import osr
import re
# from joblib import Parallel, delayed
# import multiprocessing

# Set the input data:
i = 'data/onsetcess/'
o = 'data/sp_output/'
os.makedirs(o, exist_ok=True)

xmin = float(sys.argv[1])
xmax = float(sys.argv[3])
ymin = float(sys.argv[4])
ymax = float(sys.argv[2])

print('Dataset of: ' + str(len(np.arange(xmin, xmax, 0.05))) + ' x ' + str(len(np.arange(ymin, ymax, 0.05))) + ' dimensions.')

# Create arrays for lat and lon
xlen = np.arange(xmin, xmax, 0.05)
ylen = np.arange(ymin, ymax, 0.05)

# Get list of OCL result txt files
path, dirs, files = next(os.walk(i))
# Order filenames using: https://blog.codinghorror.com/sorting-for-humans-natural-sort-order/
convert = lambda text: int(text) if text.isdigit() else text
alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
files.sort( key=alphanum_key )

# Create year list
years = []
for l in open(str(i) + str(files[0])):
  y = l.split('   ')[0].replace('\n', '')
  years.append(y)

# Determine the bounding-box of the AOI:
src = gdal.Open('data/chirps.nc')
ulx, xres, xskew, uly, yskew, yres  = src.GetGeoTransform()
# define a output format
drv = gdal.GetDriverByName("GTiff")

# Create dictionary for each year
onset = dict.fromkeys(years)
for k in onset.keys():
  onset[k] = np.zeros(shape=(len(ylen),len(xlen)))
  drv.Create("data/sp_output/onset_" + str(k) + ".tif", len(ylen), len(xlen), 1, gdal.GDT_Float32).SetGeoTransform([ulx, xres, xskew, uly, yskew, yres])

# Process & populate GeoTIFF
f = 1
while f <= len(files):
  for x in range(len(xlen)):
    for y in range(len(ylen)):
        d = open(str(i) + 'RR_GH_' + str(f) + '_ocl.txt')#.read()
        for l in d.readlines():
          year = l.split('   ')[0].replace('\n', '')
          start = l.split('   ')[1].replace('\n', '')
          end = l.split('   ')[2].replace('\n', '')
          leng = l.split('   ')[3].replace('\n', '')
          onset[str(year)][x][y] = start
          tif = gdal.Open("data/sp_output/onset_" + str(year) + ".tif", gdal.GA_Update)
          tif.GetRasterBand(1).WriteArray(onset[str(year)])
          tif.FlushCache()
          # cess[x][y] = end
          # length[x][y] = leng
        f = f + 1
