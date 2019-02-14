% do_matlab2netCDF.m
%
% Example script to convert a matlab data struct into netCDF.
% by Patrick Dickhudt, 19-apr-2017

% specify location, filenames, index

fld = 'D:\Pats_files\FDIF\netCDFcode';  % folder with everything for this example

if(1)
    globalyml = 'simple.yml';
    globalyml = 'FRF_waterquality_metadata_CS03-Microcat.yml';  % global yml file name
    instyml = 'waterquality_Microcat.yml';   % instrument yml file name
    datafn = 'FRF-ocean_waterquality_CS03-Microcat_201701.mat';  % data filename,
elseif(0)
    globalyml = 'FRF_wave_metadata_CS01-SBE26.yml';  % global yml file name
    instyml = 'waves1DCS.yml';   % instrument yml file name
    datafn = 'FRF-ocean_waves_CS01-SBE26_201701.mat';  % data filename,
end

index = 1;  % this tells it to make a new file as opposed to appending to existing

% make variables with full path and filenames
outputfn = [globalyml(1:end-4) '.nc'];   % output netcdf filename, can be whatever you want
datafile = fullfile(fld,datafn); 
metadata = fullfile(fld,globalyml);  % global yml full path and file name
template = fullfile(fld,instyml);    % instrument yml full path and file name
output_file = fullfile(fld,outputfn);  % output netcdf full path and filename

% load data struct and call matlab2netCDF function
datain = load(datafile);  % load data, in my files the data file contains a single struct whos name varies by instrument
fldnm = fieldnames(datain);  % get the name of file specific data struct
data = datain.(fldnm{1});  % put data struct into variable called data, I just did this to make it easy to try different instrument data / yml files

% make netCDF file
matlab2netCDF(data, metadata, template, index, output_file)