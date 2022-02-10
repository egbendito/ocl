#!/bin/bash
cd data/

# Prepare directory outputs
mkdir raw/
mkdir sub/
rm -rf sub/*

# Define AOI
xmin=-3.5
xmax=1.5
ymin=4.5
ymax=12

# Loop through years with 4 (n) parallel processes
for i in $(seq 1981 4 2019)
do
  # Run 4 parallel downloads
  wget https://data.chc.ucsb.edu/products/CHIRPS-2.0/global_daily/netcdf/p05/chirps-v2.0.$i.days_p05.nc raw/ &
  wget https://data.chc.ucsb.edu/products/CHIRPS-2.0/global_daily/netcdf/p05/chirps-v2.0.$(($i+1)).days_p05.nc raw/ &
  wget https://data.chc.ucsb.edu/products/CHIRPS-2.0/global_daily/netcdf/p05/chirps-v2.0.$(($i+2)).days_p05.nc raw/ &
  wget https://data.chc.ucsb.edu/products/CHIRPS-2.0/global_daily/netcdf/p05/chirps-v2.0.$(($i+3)).days_p05.nc raw/
  wait
  # Run 4 parallel subsets for the AOI
  gdal_translate -a_srs 'EPSG:4326' -projwin $xmin $ymax $xmax $ymin -projwin_srs 'EPSG:4326' -of netCDF raw/chirps-v2.0.$(($i)).days_p05.nc sub/sub_chirps-v2.0.$(($i)).days_p05_4326.nc &
  gdal_translate -a_srs 'EPSG:4326' -projwin $xmin $ymax $xmax $ymin -projwin_srs 'EPSG:4326' -of netCDF raw/chirps-v2.0.$(($i+1)).days_p05.nc sub/sub_chirps-v2.0.$(($i+1)).days_p05_4326.nc &
  gdal_translate -a_srs 'EPSG:4326' -projwin $xmin $ymax $xmax $ymin -projwin_srs 'EPSG:4326' -of netCDF raw/chirps-v2.0.$(($i+2)).days_p05.nc sub/sub_chirps-v2.0.$(($i+2)).days_p05_4326.nc &
  gdal_translate -a_srs 'EPSG:4326' -projwin $xmin $ymax $xmax $ymin -projwin_srs 'EPSG:4326' -of netCDF raw/chirps-v2.0.$(($i+3)).days_p05.nc sub/sub_chirps-v2.0.$(($i+3)).days_p05_4326.nc
  wait
done

# Use NCO (Operators for NetCDF files) https://github.com/nco/nco
ncrcat sub/*.nc ../chirps.nc

wait

# Run the python data extraction
python3 ./Data_extract.py $xmin $ymax $xmax $ymin

wait

./ocl_ranfall_ed_ver.sh

exit
