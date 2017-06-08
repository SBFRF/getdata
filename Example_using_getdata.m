%% data from records recording both wind and wave from the thredds server 
% at the USACE FRF 
% Written by Spicer Bak, 10/26/15

%% global variables
d1= datenum(2016,1,1);
d2= datenum(2016,1,3);

%end global variables
%% main code
winddata=getwind(d1,d2,1); 
wavedata=getwave(d1,d2,3);  
WLdata=getWL(d1,d2,1);     
plot(wavedata.time, wavedata.Hs)