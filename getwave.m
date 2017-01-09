function [wave] = getwave(d1, d2, gnum);
% %     function takes gauge number and returns data from FDIF server quick version in matlab based on that done in python
%   This function grabs data from the THREDDS server at CHL(2) for waves.
%   This code is meant to be used as an example, throurgh debugging has not been done
%   for this set of scripts.  The more complete version exists in python for the coastal model 
%   Test Bed (CMTB) 
%   Written by: Spicer Bak, PhD
%   email: Spicer.bak@usace.army.mil
%   
%   
%     INPUTS
%       d1=datenum(2015,10,3); example
%       d2=datenum(2015,10,4); example
%       svrloc: 


%       gnum:  gauge number of interset 
%         1 = waverider 430  - 26 m
%         2 = waverider 630  - 17 m 
%         others exist please visit 
%         http://chlthredds.erdc.dren.mil/thredds/catalog/frf/catalog.html 
%         or 
%         http://134.164.129.55/thredds/catalog/FRF/catalog.html
%         to find other gauges of interest
% 
%     RETURNS
%        data structure data with data inside

%% Matlab Get Data function start
if d2<d1
    print ' your times are backwards'
    return 
end

svrloc='https://chlthredds.erdc.dren.mil/thredds/dodsC/frf/';  % The prefix for the CHL thredds server


% add other wave gauges here
if gnum==1;
    urlback='oceanography/waves/waverider-26m/waverider-26m.ncmll'; %26 m wavericder
elseif gnum==2;
    urlback='oceanography/waves/waverider630/waverider-17m.ncml'; % 17 m waverider
elseif gnum==3;
    urlback='/oceanography/waves/awac05/awac6m.ncml' % Jennettes' pier
else;
    disp ' go to http://chlthredds.erdc.dren.mil/thredds/catalog/frf/catalog.html and browse to the gauge of interest and select the openDAP link'
end
url=strcat(svrloc,urlback);
%% Main program
time=ncread(url,'time'); % downloading time from server
%tunit= ncreadatt(url,'time','units'); % reading attributes of variable time  # how to read an attribute
% converting time to matlab datetime
mtime=time/(3600.0*24)+datenum(1970,1,1);
sprintf('Parsing time\nWave Record at this location starts: %s  ends: %s',datestr(min(mtime)),datestr(max(mtime)))
% finding index that corresponds to dates of interest
itime=find(d1 < mtime & d2> mtime); % indicies in netCDF record of data of interest
sprintf('Retieving Data')
% pulling data that is time length dependent (D1,D2)
if ~isempty(itime)
    wave.time=mtime(itime);  % record of wave time indicies in matlab datetime format
    wave.Hs=ncread(url,'waveHs',min(itime),length(itime));
    wave.fp=ncread(url,'waveFp',min(itime),length(itime));
    wave.Dp=ncread(url,'waveDp',min(itime),length(itime));
    wave.spec=permute(ncread( url, 'directionalWaveEnergyDensity' , [1,1,min(itime)],[inf,inf,length(itime)]),[3, 1, 2]); % arranging with hours in first index
    wave.Dirp=ncread(url,'waveDp',min(itime),length(itime));
    wave.spec1D=permute(ncread(url,'waveEnergyDensity',[1,min(itime)],[inf,length(itime)]),[2, 1]); % arraging with hours in first value
    %non time scale dependent variables
    wave.frqbin=ncread(url,'waveFrequency');
    wave.dirbin=ncread(url,'waveDirectionBins');
    wave.depth=ncread(url,'depth');
    wave.lat=ncread(url,'lat');
    wave.lon=ncread(url,'lon');
    wave.station_name=ncreadatt(url,'/','title');
    disp 'Data successfully grabbed'
else
    wave.time=0;
    wave.error= 'There''s no wave data at%s during %s to %s', ncreadatt(url,'/','station_name'), datestr(d1), datestr(d2);
    sprintf('There''s no wave data at%s during %s to %s\nTry another gauge' ,ncreadatt(url,'/','title'), datestr(d1), datestr(d2))
end
