#!/bin/bash

# Prepare directory outputs
mkdir raw/
mkdir sub/
rm -rf sub/*

# Define AOI
xmin=7
xmax=10
ymin=10
ymax=13

# Loop through years with 4 (n) parallel processes
for i in $(seq 1981 8 2019)
do
  # Run N parallel downloads
  wget https://data.chc.ucsb.edu/products/CHIRPS-2.0/global_daily/netcdf/p05/chirps-v2.0.$i.days_p05.nc data/raw/ &
  wget https://data.chc.ucsb.edu/products/CHIRPS-2.0/global_daily/netcdf/p05/chirps-v2.0.$(($i+1)).days_p05.nc data/raw/ &
  wget https://data.chc.ucsb.edu/products/CHIRPS-2.0/global_daily/netcdf/p05/chirps-v2.0.$(($i+2)).days_p05.nc data/raw/ &
  wget https://data.chc.ucsb.edu/products/CHIRPS-2.0/global_daily/netcdf/p05/chirps-v2.0.$(($i+3)).days_p05.nc data/raw/ &
  wget https://data.chc.ucsb.edu/products/CHIRPS-2.0/global_daily/netcdf/p05/chirps-v2.0.$(($i+4)).days_p05.nc data/raw/ &
  wget https://data.chc.ucsb.edu/products/CHIRPS-2.0/global_daily/netcdf/p05/chirps-v2.0.$(($i+5)).days_p05.nc data/raw/ &
  wget https://data.chc.ucsb.edu/products/CHIRPS-2.0/global_daily/netcdf/p05/chirps-v2.0.$(($i+6)).days_p05.nc data/raw/ &
  wget https://data.chc.ucsb.edu/products/CHIRPS-2.0/global_daily/netcdf/p05/chirps-v2.0.$(($i+7)).days_p05.nc data/raw/
  wait
  # Run N parallel subsets for the AOI
  gdal_translate -a_srs 'EPSG:4326' -projwin $xmin $ymax $xmax $ymin -projwin_srs 'EPSG:4326' -of netCDF data/raw/chirps-v2.0.$(($i)).days_p05.nc data/sub/sub_chirps-v2.0.$(($i)).days_p05_4326.nc &
  gdal_translate -a_srs 'EPSG:4326' -projwin $xmin $ymax $xmax $ymin -projwin_srs 'EPSG:4326' -of netCDF data/raw/chirps-v2.0.$(($i+1)).days_p05.nc data/sub/sub_chirps-v2.0.$(($i+1)).days_p05_4326.nc &
  gdal_translate -a_srs 'EPSG:4326' -projwin $xmin $ymax $xmax $ymin -projwin_srs 'EPSG:4326' -of netCDF data/raw/chirps-v2.0.$(($i+2)).days_p05.nc data/sub/sub_chirps-v2.0.$(($i+2)).days_p05_4326.nc &
  gdal_translate -a_srs 'EPSG:4326' -projwin $xmin $ymax $xmax $ymin -projwin_srs 'EPSG:4326' -of netCDF data/raw/chirps-v2.0.$(($i+3)).days_p05.nc data/sub/sub_chirps-v2.0.$(($i+3)).days_p05_4326.nc &
  gdal_translate -a_srs 'EPSG:4326' -projwin $xmin $ymax $xmax $ymin -projwin_srs 'EPSG:4326' -of netCDF data/raw/chirps-v2.0.$(($i+4)).days_p05.nc data/sub/sub_chirps-v2.0.$(($i+4)).days_p05_4326.nc &
  gdal_translate -a_srs 'EPSG:4326' -projwin $xmin $ymax $xmax $ymin -projwin_srs 'EPSG:4326' -of netCDF data/raw/chirps-v2.0.$(($i+5)).days_p05.nc data/sub/sub_chirps-v2.0.$(($i+5)).days_p05_4326.nc &
  gdal_translate -a_srs 'EPSG:4326' -projwin $xmin $ymax $xmax $ymin -projwin_srs 'EPSG:4326' -of netCDF data/raw/chirps-v2.0.$(($i+6)).days_p05.nc data/sub/sub_chirps-v2.0.$(($i+6)).days_p05_4326.nc &
  gdal_translate -a_srs 'EPSG:4326' -projwin $xmin $ymax $xmax $ymin -projwin_srs 'EPSG:4326' -of netCDF data/raw/chirps-v2.0.$(($i+7)).days_p05.nc data/sub/sub_chirps-v2.0.$(($i+7)).days_p05_4326.nc
  wait
done

# Use NCO (Operators for NetCDF files) https://github.com/nco/nco
ncecat data/sub/*.nc data/chirps.nc

wait

mkdir data/All_grids_data
mkdir data/onsetcess

# Run the python data extraction
python3 ./Data_extract.py $xmin $ymax $xmax $ymin

wait

# Run the shell script for computing onset, cessation and length of the season
./ocl_ranfall_ed_ver.sh

wait

# Create GeoTIFF for outputs
mkdir data/spatial
python3 ./Data_sp.py $xmin $ymax $xmax $ymin


exit
