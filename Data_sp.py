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
o = 'data/spatial/'
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
  drv.Create(str(o) + "onset_" + str(k) + ".tif", len(xlen), len(ylen), 1, gdal.GDT_Float32).SetGeoTransform([ulx, xres, 0, uly, 0, yres]) # Need to invert the vertical resolution since we are starting from the top-left corner, and going downwards
cess = dict.fromkeys(years)
for k in cess.keys():
  cess[k] = np.zeros(shape=(len(ylen),len(xlen)))
  drv.Create(str(o) + "cessation_" + str(k) + ".tif", len(xlen), len(ylen), 1, gdal.GDT_Float32).SetGeoTransform([ulx, xres, 0, uly, 0, yres]) # Need to invert the vertical resolution since we are starting from the top-left corner, and going downwards
leng = dict.fromkeys(years)
for k in leng.keys():
  leng[k] = np.zeros(shape=(len(ylen),len(xlen)))
  drv.Create(str(o) + "length_" + str(k) + ".tif", len(xlen), len(ylen), 1, gdal.GDT_Float32).SetGeoTransform([ulx, xres, 0, uly, 0, yres]) # Need to invert the vertical resolution since we are starting from the top-left corner, and going downwards

# Process & populate GeoTIFF
f = 1
while f <= len(files):
  for y in range(len(ylen)):
    for x in range(len(xlen)):
      d = open(str(i) + 'RR_' + str(f) + '_ocl.txt')#.read()
      for l in d.readlines():
        year = l.split('   ')[0].replace('\n', '')
        start = l.split('   ')[1].replace('\n', '')
        onset[str(year)][y][x] = start
        tif = gdal.Open(str(o) + "onset_" + str(year) + ".tif", gdal.GA_Update)
        tif.GetRasterBand(1).WriteArray(onset[str(year)])
        tif.FlushCache()
      f = f + 1

# Process & populate GeoTIFF
f = 1
while f <= len(files):
  for y in range(len(ylen)):
    for x in range(len(xlen)):
        d = open(str(i) + 'RR_' + str(f) + '_ocl.txt')#.read()
        for l in d.readlines():
          year = l.split('   ')[0].replace('\n', '')
          end = l.split('   ')[2].replace('\n', '')
          cess[str(year)][y][x] = end
          tif = gdal.Open(str(o) + "cessation_" + str(year) + ".tif", gdal.GA_Update)
          tif.GetRasterBand(1).WriteArray(cess[str(year)])
          tif.FlushCache()
        f = f + 1

# Process & populate GeoTIFF
f = 1
while f <= len(files):
  for y in range(len(ylen)):
    for x in range(len(xlen)):
        d = open(str(i) + 'RR_' + str(f) + '_ocl.txt')#.read()
        for l in d.readlines():
          year = l.split('   ')[0].replace('\n', '')
          le = l.split('   ')[2].replace('\n', '')
          leng[str(year)][y][x] = le
          tif = gdal.Open(str(o) + "length_" + str(year) + ".tif", gdal.GA_Update)
          tif.GetRasterBand(1).WriteArray(leng[str(year)])
          tif.FlushCache()
        f = f + 1
