#!/bin/bash
# cd data/raw/
# for i in $(seq 1981 1 2019)
for i in $(seq 2016 4 2019)
do
  # wget https://data.chc.ucsb.edu/products/CHIRPS-2.0/global_daily/netcdf/p05/chirps-v2.0.$i.days_p05.nc
  # gdal_translate -a_srs 'EPSG:4326' -projwin -3.5 12 1.5 4.5 -projwin_srs 'EPSG:4326' -of netCDF data/raw/chirps-v2.0.$i.days_p05.nc data/GHA/GHA_chirps-v2.0.$i.days_p05_4326.nc
  # echo $i
  # echo $(($i+1))
  # echo $(($i+2))
  # echo $(($i+3))
  # sleep 1
  gdal_translate -a_srs 'EPSG:4326' -projwin -3.5 12 1.5 4.5 -projwin_srs 'EPSG:4326' -of netCDF data/raw/chirps-v2.0.$(($i)).days_p05.nc data/GHA/GHA_chirps-v2.0.$(($i)).days_p05_4326.nc &
  gdal_translate -a_srs 'EPSG:4326' -projwin -3.5 12 1.5 4.5 -projwin_srs 'EPSG:4326' -of netCDF data/raw/chirps-v2.0.$(($i+1)).days_p05.nc data/GHA/GHA_chirps-v2.0.$(($i+1)).days_p05_4326.nc &
  gdal_translate -a_srs 'EPSG:4326' -projwin -3.5 12 1.5 4.5 -projwin_srs 'EPSG:4326' -of netCDF data/raw/chirps-v2.0.$(($i+2)).days_p05.nc data/GHA/GHA_chirps-v2.0.$(($i+2)).days_p05_4326.nc &
  gdal_translate -a_srs 'EPSG:4326' -projwin -3.5 12 1.5 4.5 -projwin_srs 'EPSG:4326' -of netCDF data/raw/chirps-v2.0.$(($i+3)).days_p05.nc data/GHA/GHA_chirps-v2.0.$(($i+3)).days_p05_4326.nc
  # # gdal_translate -a_srs 'EPSG:4326' -projwin -3.5 12 1.5 4.5 -projwin_srs 'EPSG:4326' -of netCDF data/raw/chirps-v2.0.$(($i+4)).days_p05.nc data/GHA/GHA_chirps-v2.0.$(($i+4)).days_p05_4326.nc &
  # # gdal_translate -a_srs 'EPSG:4326' -projwin -3.5 12 1.5 4.5 -projwin_srs 'EPSG:4326' -of netCDF data/raw/chirps-v2.0.$(($i+5)).days_p05.nc data/GHA/GHA_chirps-v2.0.$(($i+5)).days_p05_4326.nc
  wait
done
exit
