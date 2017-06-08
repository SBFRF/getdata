# this is an example of how to get FRF data utilizing a wget command from bash

# first set the year 
year=2016  # here
for month in 01 02 03 04 05 06 07 08 09 10 11 12  # next we'll loop over all 12 months, downloading each month of data
do # do this on the loop execution
# esentially modifying the below url by year and month 
url='http://chlthredds.erdc.dren.mil/thredds/fileServer/frf/oceanography/waves/waverider-26m/'$year'/FRF-ocean_waves_waverider-26m_'$year$month'.nc'  

echo .....

wget $url  # wgeting on that data 
done