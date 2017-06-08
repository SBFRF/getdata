function [ wind ] = getwind( d1, d2, gnum)
% %     function takes gauge number and returns data from FDIF server quick version in matlab based on that done in python
%   This function grabs data from the THREDDS server at the FRF (1) or CHL(2) for waves.
%   This code is meant to be used as an example, throurgh debugging has not been done
%   for this set of scripts.  The more complete version exists in python for the coastal model 
%   Test Bed (CMTB) 
%   Written by: Spicer Bak, PhD
%   email: Spicer.bak@usace.army.mil
%
%   INPUTS 
%       d1-start date in matlab datenum format - ex. datenum(2015,10,2)
%       d2-end date in matlab datenum format - see above
%       gnum is the gauge number 
%   	1 = Derived winds (best product)
%       2 = Gauge 932


%% setup 
svrloc='http://chlthredds.erdc.dren.mil/thredds/dodsC/frf/';  % The prefix for the CHL thredds server

if gnum==1;
    urlback='meteorology/wind/derived/derived.ncml'; % derived wind record  
elseif gnum==2;
    urlback='meteorology/wind/D932/D932.ncml'; % local thredds Digital collect 932  _ back end for specific gauge ncml
    print 'guage selcected is 932 Digital collection' 
else;
    disp ' go to http://chlthredds.erdc.dren.mil/thredds/catalog/frf/catalog.html and browse to the gauge of interest and select the openDAP link'
end
url=strcat(svrloc,urlback);
%% Main Program
time=ncread(url,'time'); % downloading time from server
tunit= ncreadatt(url,'time','units'); % reading attributes of variable time
% converting time to matlab datetime
mtime=time/(3600.0*24)+datenum(1970,1,1);
% finding index that corresponds to dates of interest
sprintf('this wind record starts %s and ends %s', datestr(min(mtime)),datestr(max(mtime)))
itime=find(d1 < mtime & d2> mtime); % indicies in netCDF record of data of interest
% itime could probably be done faster with a boolean
% pulling wind data 
if ~isempty(itime)
    wind.time=mtime(itime);  % record of wind time indicies in matlab datetime format
    wind.spd=ncread(url,'windSpeed',min(itime),length(itime));
    wind.vecspd=ncread(url,'vectorSpeed',min(itime),length(itime));
    wind.sustwindspd=ncread(url,'sustWindSpeed',min(itime),length(itime));
    wind.windgust=ncread(url,'windGust',min(itime),length(itime));
    wind.winddir=ncread(url,'windDirection',min(itime),length(itime));
    wind.maxwindspeed=ncread(url,'maxWindSpeed',min(itime),length(itime));
    wind.minwindspeed=ncread(url,'minWindSpeed',min(itime),length(itime));
    wind.stdWindSpeed=ncread(url,'stdWindSpeed',min(itime),length(itime));
    wind.qcflag=ncread(url,'qcFlag',min(itime),length(itime));
    % non time  dependent variables
    wind.lat=ncread(url,'lat');
    wind.lon=ncread(url,'lon');
    wind.station_name=ncread(url,'station_name');
else
    wind.time=0;
    wind.error='There''s no data in this time frame on the server';
    disp 'no Wind Data'
end

