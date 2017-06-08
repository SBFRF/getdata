import netCDF4 as nc # library for handling netCDF files 
import datetime as DT # general date handling, similar to matlab date vec 
import numpy as np   # general math library

d1 = DT.datetime(2015,10,01,12,0 )  # set start time of data query here 
d2 = DT.datetime(2015,10,02,0,0)    # set end time of data querey here

serverLocation = 'http://chlthredds.erdc.dren.mil/thredds/dodsC/frf'  # the www.CHLthredds.erdc.dren.mil/thredds/catalog.htm  website
dataLoc = '/oceanography/waves/waverider-26m/waverider-26m.ncml'  # the gauge extension for 26 m waverider  - this is what i vary when i want a different gauge

ncfile = nc.Dataset(serverLocation + dataLoc)  # this loads the netCDF file but no data 
tt = ncfile['time'][:]  # This loads all of the time from the 26m ncml file in epoch time,
# the [:] distinguish's between the meta data or the actual data, ncfile['time'] will retrieve the time variables meta data (& data)
# where ncfile['time'][:] accesses just the data
time = nc.num2date(ncfile['time'][:], ncfile['time'].units)
# here the .units call access the variable attibute units (in the metadata), the value of this is a string that reads 'seconds since 1970-01-01'
mask = (time >= d1) & (time < d2)  # returns an array of true/false of length (time)
idx = np.argwhere(mask)[0]  # return the indicies of True

# This is the more explicit version of the above (more matlab-esc)
# This version assumes user knows names of the variables or cares to rename eg waveDirectionPeakFrequency -> waveDp
wavespec = {'time' :       time,
            'name':        str(ncfile.title),
            'wavefreqbin': ncfile['waveFrequency'][:],
            'lat':         ncfile['lat'][:],
            'lon':         ncfile['lon'][:], # 
            'depth':       ncfile['depth'],  # not dimensioned in time
            'Hs':          ncfile['waveHs'][idx],  # dimensioned in time 
            'peakf' :      ncfile['wavePeakFrequency'][idx],
            'wavedirbin':  ncfile['waveDirectionBins'][:],
            'dWED':        ncfile['directionalWaveEnergyDensity'][idx, :, :],
            'waveDp':      ncfile['wavePeakDirectionPeakFrequency'][idx],
            'waveDm':      ncfile['waveMeanDirection'][idx],
            'qcFlagE':     ncfile['qcFlagE'][idx],
            'qcFlagD':     ncfile['qcFlagD'][idx],
    }