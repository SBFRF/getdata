# What’s in a netCDF file:
_written by Patrick Dickhudt, with edits from Spicer Bak _
_This document describes pat's package, a helpful tool in attached folder_ 

## To take a quick look at an included netCDF with Matlab:

_ncn = 'FRF_wave_metadata_CS01-SBE26.nc';_  % file name, add full path if not in current directory
`ncdisp(ncn)`;  % this is a way to take a quick look at what’s in a file, will spit out all attributes, dimensions, and variables (but not the data) to the command line

__Global attributes:__ These are meant to apply to all data contained in the file and often include things like where the data was collected (e.g. lat, lon, depth), what instrument (e.g. make, model, serial number), and really anything else you as a data provider would want a user to know (e.g. summary, “This data was collected as part of whatever project, in whatever facility, …). These are specified in a global attributes `*.yml` file.  A list of example global yml files is below. 

__Dimensions:__ These specify the size of your data variables.  If you just have time series data, you only need 1 dimension, time.  If you have time series profile data (e.g. ADCP) you might have 2 dimensions, time and depth.  Not every data variable has to have every dimension. For example, with ADCP data, the pressure data may just have dimension time while current profiles have dimensions time and depth (or distance from transducer or whatever is appropriate). Our convention (and a very common one) is that time is the only unlimited dimension. Unlimited dimensions can change size (for example if you want to append data).  The size of all other dimensions is fixed at what you originally specify for a given netCDF.  This is all done behind the scenes in the conversion code but is good to be aware of. Note: our files have dimension station_name_length which is weird and is something that is for some reason required for our data portal.  

__Variables:__  The data.  Variables also have metadata including size, dimension, datatype, and attributes.  The variables to be output as well as the variable attributes are specified in the instrument .yml file. A list of included example instrument yml files is below.

__Note on time:__ We have been converting time from Matlab datenum (the time in your data struct should be Matlab datenum) to epoch time (seconds since 1970-01-01 00:00:00).  This code automatically does that conversion when generating a netCDF file.  I have included `epoch2Matlab.m` which will convert it back for you.  


## yml files

Basically a text file with standard formatting.  I’ve found that most text editors handle them OK but not perfect.  Mixed up formatting can cause the netCDF conversion to crash.

__Global yml files:__
Specifies the global attributes. This can include whatever you want it to. One of the requirements for our data to get onto our data portal is that we have title as a global attribute.  We can remove this from the code but I have not done so.  This also makes a dimension called `station_name_length` that stores an array of characters, that can be annoying at times, but there are ways to handle it
 A lot of people have spent a lot of time thinking about this.  If you want to see some guidance:
https://www.unidata.ucar.edu/software/thredds/current/netcdf-java/metadata/DataDiscoveryAttConvention.html

__Example files for reference:__
_FRF_wave_metadata_CS01-SBE26.yml_
_FRF_waveMetadata_xp125m.yml_
_FRF_current_metadata_CS01-ADOP.yml_ – note, I don’t think this one will run if you try.  The data file I included needs to be run through 1 other program before its ready to covert.
_FRF_waterlevel_metadata_CS01-SBE26.yml_
_FRF_waterquality_metadata_CS03-Microcat.yml_

## Variable yml files:
This provides guidance to `matlab2netCDF.m` informing what variables to include from the data struct, any additional attributes found in the data struct that should be added to the global attributes, what dimensions are included, what to call the data struct variables in the netCDF file (you can use this to convert names), and variable attributes.

### Parts of variable yml files:
`_variables:` ['time', 'lat', 'lon', 'station_name', 'hs', 'fp', 'specS', 'freq', 'depth', 'depthP', 'qcFlagE']
This specifies which fields to pull from the data struct and make into variables.  You don’t have to include all fields in the data struct in the netCDF.

`_attributes:` ['Station', 'manufacturer', 'model', 'serialNumber']_
This specifies which fields to pull from the data struct and add to the global attributes.  The name of the field will also be the name of the global attribute.

`_dimensions:` ['time', 'freq','station_name_length']_
Specifies dimensions

_Specifying variable names and attributes_
`    time:
        name: 'time'
        units: 'seconds since 1970-01-01 00:00:00'
        standard_name: 'time'
        long_name: 'UTC Sample Time'
        data_type: 'f8'  
        dim: ['time']
        calendar: 'gregorian'
        fill_value: '-999'`

This provides information about the variables.

_time:_
Specifies the name of the data field in the data struct
_name: 'time'_
Specifies what to call it in the netCDF file.  In this case it is called time in the data struct and will be called time in the output netCDF file. 

Another example:
_hs:
    name: 'waveHs'
    units: 'm'
    standard_name: 'sea_surface_wave_significant_height'
    long_name: 'Significant Wave Height'
    data_type: 'f4'
    dim: ['time']
    fill_value: '-999'
    short_name: 'Wave Height'
    coordinates: 'lat lon'_

_hs:_
Specifies the name of the data field in the data struct
_name: 'waveHs'_
Specifies what to call it in the netCDF file.  In this case it is called hs in the data struct and will be called waveHs in the output netCDF file. 

Example files for reference: 
_currents.yml_
_waterquality_Microcat.yml_
_waves1DCS.yml_




## mfiles
_do_matlab2netCDF.m_
	Script I threw together to run a couple examples.  Pretty sure I included all the necessary files. You should be able to change “fld” to specify wherever you put these files and it will run.

_matlab2netCDF.m_
	Function that does the conversion from Matlab struct to netCDF.

_ymlGetMeta.m_
	Something I wrote that you may find helpful.  I use this when I want to put something in a yml file where it gets preserved in my netCDF but also want to use it in my initial processing.  For example, an offset, instrument elevation, etc.  I use it like this:
_metget = {‘offset’, ’elevation’};_   this specifies what I want to pull from the yml file. In the yml file would look like `offset: value` and `elevation: value`.
_metgot = ymlGetMeta(ymlFile,metget);_
I can put it into my data struct like this:
_for i = 1:length(metget)
        data.(metget{i}) = metgot{i};
 end_

_epoch2Matlab.m_
	Convert epoch time to Matlab datenum.  

The remaining .m files are used by matlab2netCDF.m.


# Accessing data from netCDF
Matlab has built in functions and the help is pretty good.  Here are a few examples to get you started:
ncn = 'FRF_wave_metadata_CS01-SBE26.nc';    % file name, add full path if not in current directory
`ncdisp(ncn);`  % this is a way to take a quick look at what’s in a file, will spit out all attributes, dimensions, and variables (but not the data) to the command line
`t = ncread(ncn, 'time');`  % get the time vector
`dn = epoch2Matlab(t);` % convert to Matlab datenum
`hs = ncread(ncn,'waveHs');`  % read some data, in this case variable waveHs

