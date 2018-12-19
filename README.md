# getdata

Our server is here: https://chlthredds.erdc.dren.mil/thredds  (please note the https)  If you're a matlab user, this can cause problems (see below).  All of our data are stored in netCDF files which work wonderfully with the THREDDS server architecture.  
The data on the server are laid out pretty intuitively (I hope) so feel free to click around, but a few of the data you may be most interested in are listed below.  The ncml files act as automatic concatenation scripts which allow one access point for all of the data (this is the easiest).  OPeNDAP is likely where you're interested in 'browsing' through the data and metadata. It is also the easiest way to 'drop' data into your workspace (regardless of language). 
Amongst other things, the matlab issue is explained here with bug reports and fixes 

To compliment this repository, I also have a pretty robust python package here to interact with our data: https://github.com/erdc/getdatatestbed which is actively developed on another forked repository. 

Example codes for FRF Thredds data access for matlab and python, and bash.  Other simple examples in other languages are welcome for contribution.

#######################
Matlab:
#######################

There is a matlab version composed of functions: 
getWL, getwave, getwind.  To run these versions an example script has been written called Example_using_getdata.m

This script will use the three functions to get the data and return them in mat structures with an associated start
and end date (d1, d2)  where d1 is inclusive and d2 is exclusive

please note, there are issues regarding matlab and accessing https servers.  This seems to be resolved in 2017a.  please refer to the following link to matlab's bug support for a solution. 
https://www.mathworks.com/support/bugreports/1072120

#######################
Python:
#######################


Commented out python code to load the netCDF file and parse the time to select appropriate wave data
our friends at deltares have a nice readme on how to access data from thredds server via openDAP protocol on opening netCDF files 
https://publicwiki.deltares.nl/display/OET/Reading+data+from+OpenDAP+using+python

please contact spicer.bak@usace.army.mil for any questions or concerns
