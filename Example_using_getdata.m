%% data from records recording both wind and wave from the thredds server 
% at the USACE FRF 
% Written by Spicer Bak, 10/26/15

%% global variables
d1= datenum(2016,1,1);
d2= datenum(2016,1,3);

%end global variables
%% main code (d1, d2, gauge number, server locations)
winddata=getwind(d1,d2,1,2);  % at the time written, wind data only on frf server (.,.,.,2)
wavedata=getwave(d1,d2,1,2);  % at the time written, wave data only on frf server (.,.,.,2)
WLdata=getWL(d1,d2,1,2);      % at the time written, WL data only on frf server (.,.,.,2)
plot(wavedata.time, wavedata.Hs)