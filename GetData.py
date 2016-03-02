# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 13:38:05 2015
This is a class definition designed to get data from the FRF thredds server 

@author: Spicer Bak, PhD
@contact: spicer.bak@usace.army.mil
@organization: USACE CHL FRF


"""
import netCDF4 as nc
import datetime as DT
import numpy as np

class GetData:
    """
    Note d1 and d2 have to be in date-time formats 
    are all data set times in UTC?
    need to write error handling, what to do if there's no data ?? 
    
    """

    def __init__(self, d1, d2):
        """        
        Initialization description here
        Data are returned in self.datainex are inclusive at d1,d2
        Data comes from waverider 632 (26m?)
        """

        self.rawdataloc_wave = []
        self.outputdir = 'C:/users/u4hncasb/Documents/STWave/live/output/'  # location for outputfiles
        self.d1 = d1  # start date for data grab
        self.d2 = d2  # end data for data grab
        self.timeunits = 'seconds since 1970-01-01 00:00:00'
        self.epochd1 = nc.date2num(self.d1, self.timeunits)
        self.epochd2 = nc.date2num(self.d2, self.timeunits)
        self.comp_time()
        self.frfdataloc = 'http://134.164.129.55/thredds/dodsC/FRF/'
        self.wisdataloc = 'http://chlthredds.erdc.dren.mil/thredds/dodsC/frf/'
        assert type(self.d2) == DT.datetime, 'd1 need to be in python "Datetime" data types'
        assert type(self.d1) == DT.datetime, 'd2 need to be in python "Datetime" data types'

    def comp_time(self):
        """ 
        Test if times are backwards
        """
        assert self.d2 >= self.d1, 'finish time: d2 needs to be after start time: d1'

    def roundtime(self, dt=None, roundto=60):
        """
        Round a datetime object to any time laps in seconds
        Author: Thierry Husson 2012 - Use it as you want but don't blame me.
        :rtype: object

        :param dt:
            datetime.datetime object, default now.
        :param roundto:
            Closest number of SECONDS to round to, default 1 minute
        """
        if dt is None:
            dt = DT.datetime.now()
        seconds = (dt - dt.min).seconds
        # // is a floor division, not a comment on following line:
        rounding = (seconds + roundto / 2) // roundto * roundto
        return dt + DT.timedelta(0, rounding - seconds, -dt.microsecond)

    def gettime(self, dt=30):
        """
        this function opens the netcdf file, pulls down all of the time, then pulls the dates of interest
        from the THREDDS (data loc) server based on d1,d2, and data location
        it returns the indicies in the NCML file of the dates d1>=time>d2
        INPUTS:

            d1: start time - pulled from self 
            d2: end time  - pulled from self 
            dataloc: location of the data to search through
            :param dt: the time delta of the data out of interest

        """
        # TODO find a way to pull only hourly data or regular interval of desired time

        try:

            self.ncfile = nc.Dataset(self.frfdataloc + self.dataloc)
            #            try:
            self.alltime = nc.num2date(self.ncfile['time'][:], self.ncfile['time'].units,
                                       self.ncfile['time'].calendar)
            for i, date in enumerate(self.alltime):
                self.alltime[i] = self.roundtime(self.alltime[i])

            # TODO saerch through time using epochd1, d2 instead of datetime,d1,d2
            mask = (self.alltime >= self.d1) & (self.alltime < self.d2)  # boolean true/false of time
            idx = np.where(mask)[0]
            assert len(idx) > 0, 'no data locally, checking CHLthredds'
            print "Data Gathered From Local Thredds Server"
        except (RuntimeError, NameError, AssertionError):  # if theres any error try to get good data from next location
            self.ncfile = nc.Dataset(self.wisdataloc + self.dataloc)
            #            try:
            self.alltime = nc.num2date(self.ncfile['time'][:], self.ncfile['time'].units,
                                       self.ncfile['time'].calendar)

            mask = (self.alltime >= self.d1) & (self.alltime < self.d2)  # boolean true/false of time
            idx = np.where(mask)[0]

            try:
                assert len(idx) > 0, ' There are no data within the search parameters for this gauge'
                print "Data Gathered from CHL thredds Server"
            except AssertionError:
                idx = 0

        return idx


    def getwavespec(self, gaugenumber=0, collectionlength=30):
        """
        This function pulls down the data from the thredds server and puts the data into proper places
        to be read for STwave Scripts
        this will return the wavespec with dir/freq bin and directional wave energy

        TO DO:
        Set optional date input from function arguments

        :param gaugenumber:
            gaugenumber = 0, 26m wave rider
            gaugenumber = 1, 17m waverider
            gaugenumber = 2, awac4 - 11m
            gaugenumber = 3, awac3 - 8m
            gaugenumber = 4, awac2 - 6m
            gaugenumber = 5, awac1 - 5m
            gaugenumber = 6, adopp2 - 3m
            gaugenumber = 7, adopp1 - 2m
            gaugenumber = 8,  Paros xp200m
            gaugenumber = 9,  Paros xp150m
            gaugenumber = 10, Paros xp125m
            gaugenumber = 11, Paros xp100m
            gaugenumber = 12, 8 m array
        :param collectionlength:
            s the time over which the wind record exists
            ie data is collected in 10 minute increments time is rounded to nearest 10min increment
            data is rounded to the nearst [collectionlength] (default 30 min)
        """
        # Making gauges flexible

        if gaugenumber == 0:
            # 26 m wave rider
            self.dataloc = 'oceanography/waves/waverider430/waverider430.ncml'  # 26m buoy
            gname = '26m Waverider Buoy'
        elif gaugenumber == 1:
            # 2D 17m waverider
            self.dataloc = 'oceanography/waves/waverider630/waverider630.ncml'  # 17 m buoy
            gname = '17m Waverider Buoy'
        elif gaugenumber == 2:
            gname = 'AWAC04 - 11m'
            self.dataloc = 'oceanography/waves/awac04/awac04.ncml'
        elif gaugenumber == 3:
            gname = 'AWAC03 = 8m'
            self.dataloc = 'oceanography/waves/awac03/awac03.ncml'
        elif gaugenumber == 4:
            gname = 'AWAC02 - 6m'
            self.dataloc = 'oceanography/waves/awac02/awac02.ncml'
        elif gaugenumber == 5:
            gname = 'AWAC01 - 5m'
            self.dataloc = 'oceanography/waves/awac01/awac01.ncml'
        elif gaugenumber == 6:
            gname = 'Aquadopp02 - 3m'
            self.dataloc = 'oceanography/waves/adop02/adop02.ncml'
        elif gaugenumber == 7:
            gname = 'Aquadopp01 - 2m'
            self.dataloc = 'oceanography/waves/adop01/adop01.ncml'
        elif gaugenumber == 8:
            gname = 'Paros xp200m'
            self.dataloc = 'oceanography/waves/xp200m/xp200m.ncml'
        elif gaugenumber == 9:
            gname = 'Paros xp150m'
            self.dataloc = 'oceanography/waves/xp150m/xp150m.ncml'
        elif gaugenumber == 10:
            gname = 'Paros xp125m'
            self.dataloc = 'oceanography/waves/xp125m/xp125m.ncml'
        elif gaugenumber == 11:
            gname = 'Paros xp100m'
            self.dataloc = 'oceanography/waves/xp100m/xp100m.ncml'
        elif gaugenumber == 12:
            gname = "8m array"
            self.dataloc = 'oceanography/waves/8m-Array/array8m.ncml'
        else:
            gname = 'There Are no Gauge numbers here'
            print 'ERROR Specifiy proper Gauge number'
        # parsing out data of interest in time
        try:
            self.wavedataindex = self.gettime()
            # assert len(self.wavedataindex)>0,'there''s no data in your time period'

            if np.size(self.wavedataindex) > 1:
                # consistant for all wave gauges
                self.snaptime = nc.num2date(self.ncfile['time'][self.wavedataindex], self.ncfile['time'].units,
                                            self.ncfile['time'].calendar)

                for num in range(0, len(self.snaptime)):
                    self.snaptime[num] = self.roundtime(self.snaptime[num], roundto=collectionlength * 60)
#                if collectionlength != 30:
#                    self.wavedataindex=self.cliprecords(self.snaptime)
                peakf = self.ncfile['waveFp'][self.wavedataindex]
                wavefreqbin = self.ncfile['waveFrequency'][:]
                Hs = self.ncfile['waveHs'][self.wavedataindex]

                try:
                    depth = self.ncfile['depth'][:]
                except IndexError:
                    depth = self.ncfile['depthP'][-1]

                wavespec= {'time': self.snaptime,
                           'name': self.ncfile.title,
                           'wavefreqbin': wavefreqbin,
                           'lat':self.ncfile['lat'][:],
                           'lon': self.ncfile['lon'][:],
                           'depth': depth,
                           'Hs': Hs,
                           'peakf': peakf,
                           #'Tp': 1/peakf
                           }
                try:
                    wavespec['wavedirbin'] = self.ncfile['waveDirectionBins'][:]
                    wavespec['dWED'] = self.ncfile['directionalWaveEnergyDensity'][self.wavedataindex, :, :]
                    wavespec['waveDp'] = self.ncfile['waveDp'][self.wavedataindex]
                except IndexError:
                    wavespec['wavedirbin'] = range(0,360,2)
                    wavespec['dWED'] = np.zeros([len(self.wavedataindex), len(wavespec['wavefreqbin']), len(wavespec['wavedirbin'])])
                    wavespec['dWED'][:] = 1e-8
                    wavespec['waveDp'] = np.zeros(len(self.wavedataindex))
                    wavespec['WED'] = self.ncfile['waveEnergyDensity'][self.wavedataindex, :]
                    wavespec['depthp'] = self.ncfile['depthP'][self.wavedataindex]



                return wavespec
        except (RuntimeError):
            print 'ERROR:  There is no WAVE DATA for this time period\nstart: %s  End: %s  Gauge name %s' % (
            self.d1, self.d2, gname)
            wavespec = 0
            return wavespec

    def getcur(self, collectionlength=1):
        """
        This function pulls down the currents data from the Thredds Server


            :param collectionlength:
                the time over which the wind record exists
                ie data is collected in 10 minute increments
                data is rounded to the nearst [collectionlength] (default 1 min)
        """
        self.dataloc = 'oceanography/currents/awac04/awac04.ncml'

        currdataindex = self.gettime()
        # _______________________________________
        # get the actual current data
        if np.size(currdataindex) > 1:
            curr_aveU = self.ncfile['aveU'][currdataindex]  # pulling depth averaged Eastward current
            curr_aveV = self.ncfile['aveV'][currdataindex]  # pulling depth averaged Northward current
            curr_spd = self.ncfile['currentSpeed'][currdataindex]  # currents speed [m/s]
            curr_dir = self.ncfile['currentDirection'][currdataindex]  # current from direction [deg]
            curr_time = nc.num2date(self.ncfile['time'][currdataindex], self.ncfile['time'].units,
                                         self.ncfile['time'].calendar)
            for num in range(0, len(self.curr_time)):
                self.curr_time[num] = self.roundtime(self.curr_time[num], roundto=collectionlength * 60)
            self.curpacket = {
                'name': self.ncfile.title,
                'time': curr_time,
                'aveU': curr_aveU,
                'aveV': curr_aveV,
                'speed': curr_spd,
                'dir': curr_dir,
                'lat': self.ncfile['lat'][:],
                'lon': self.ncfile['lon'][:],
                'depth': self.ncfile['depth'][:],
            # Depth is calculated by: depth = -xducerD + blank + (binSize/2) + (numBins * binSize)
                'meanP': self.ncfile['meanPressure'][currdataindex],

            }
            return self.curpacket
        else:
            print 'ERROR: There is no curren data for this time period!!!'
            self.curpacket = 0
            return self.curpacket

    def getwind(self, collectionlength=10, gaugenumber=0):
        """
        this function retrieves the wind data from the FDIF server
        collection length is the time over which the wind record exists
            ie data is collected in 10 minute increments
            data is rounded to the nearst [collectionlength] (default 10 min)

            gauge 0 = 932
        """
        # Making gauges flexible
        # different Gauges
        if gaugenumber == 0:
            # 26 m wave rider
            self.dataloc = 'meteorology/wind/D932/D932.ncml'  # 932 wind gauge
            gname = '932 wind gauge '
        elif gaugenumber == 1:
            # 2D 832 wind gauge
            self.dataloc = 'meteorology/wind/D832/D832.ncml'  # 832 wind gauge
            gname = '832 wind gauge'
        elif gaugenumber == 2:
            gname = '732 wind gauge'
            self.dataloc = 'meteorology/wind/732/732.ncml'
        elif gaugenumber == 3:
            gname = '632 wind gauge'
            self.dataloc = 'meteorology/wind/632/632.ncml'
        elif gaugenumber == 4:
            gname = 'Derived'
            self.dataloc = 'meteorology/wind/derived/derived.ncml'
        else:
            self.rawdataloc_wave = []
            print '<EE>ERROR Specifiy proper Gauge number'

        self.winddataindex = self.gettime()

        # ______________________________________
        if np.size(self.winddataindex) > 0:
            windvecspd = self.ncfile['vectorSpeed'][self.winddataindex]
            windspeed = self.ncfile['windSpeed'][self.winddataindex]  # wind speed
            winddir = self.ncfile['windDirection'][self.winddataindex]  # wind direction
            windgust = self.ncfile['windGust'][self.winddataindex]  # 5 sec largest mean speed
            stdspeed = self.ncfile['stdWindSpeed'][self.winddataindex]  # std dev of 10 min avg
            qcflag = self.ncfile['qcFlag'][self.winddataindex]  # qc flag
            minspeed = self.ncfile['minWindSpeed'][self.winddataindex]  # min wind speed in 10 min avg
            maxspeed = self.ncfile['maxWindSpeed'][self.winddataindex]  # max wind speed in 10 min avg
            sustspeed = self.ncfile['sustWindSpeed'][self.winddataindex]  # 1 minute largest mean wind speed
            gaugeht = self.ncfile.geospatial_vertical_max

            self.windtime = nc.num2date(self.ncfile['time'][self.winddataindex], self.ncfile['time'].units,
                                        self.ncfile['time'].calendar)  # wind time
            for num in range(0, len(self.windtime)):
                self.windtime[num] = self.roundtime(self.windtime[num], roundto=collectionlength * 60)
            # correcting for wind elevations from Johnson (1999) - Simple Expressions for correcting wind speed data for elevation
            if gaugeht <= 20:
                windspeed_corrected = windspeed * (10 / gaugeht) ** (1 / 7)
            else:
                windspeed_corrected = 'No Corrections done for gauges over 20m, please read: \nJohnson (1999) - Simple Expressions for correcting wind speed data for elevation'
            windpacket = {
                'name': self.ncfile.title,  # station name
                'time': self.windtime,  # time
                'vecspeed': windvecspd,  # Vector Averaged Wind Speed
                'windspeed': windspeed,  # Mean Wind Speed
                'windspeed_corrected': windspeed_corrected,  # corrected windspeed
                'winddir': winddir,  # Wind direction from true nort
                'windgust': windgust,  # 5 second largest mean wind speed
                'qcflag': qcflag,  # QC flag
                'stdspeed': stdspeed,  # std dev of 10 min wind record
                'minspeed': minspeed,  # min speed in 10 min avg
                'maxspeed': maxspeed,  # max speed in 10 min avg
                'sustspeed': sustspeed,  # 1 min largest mean wind speed
                'lat': self.ncfile['lat'][:],  # latitude
                'lon': self.ncfile['lon'][:]  # longitde
                }
            return windpacket
        else:
            print 'ERROR: There is no Wind Data for this time period !!!'
            windpacket = 0
            return windpacket

    def getWL(self, collectionlength=6):
        """
        This function retrieves the water level data from the FDIF server
        WL data on server is NAVD

        collection length is the time over which the wind record exists
            ie data is collected in 10 minute increments
            data is rounded to the nearst [collectionlength] (default 6 min)
        """
        # self.WLloc='http://134.164.129.55/thredds/dodsC/FRF/oceanography/waterlevel/11/11.ncml'
        self.dataloc = 'oceanography/waterlevel/11/11.ncml'  # this is the local FRF version of the thredds server
        self.WLdataindex = self.gettime()

        if np.size(self.WLdataindex) > 1:
            self.WL = self.ncfile['waterLevelHeight'][self.WLdataindex]
            self.WLtime = nc.num2date(self.ncfile['time'][self.WLdataindex], self.ncfile['time'].units,
                                      self.ncfile['time'].calendar)
            for num in range(0, len(self.WLtime)):
                self.WLtime[num] = self.roundtime(self.WLtime[num], roundto=collectionlength * 60)

            self.WLpacket = {
                'name': self.ncfile.title,
                'WL': self.ncfile['waterLevelHeight'][self.WLdataindex],
                'time': self.WLtime,
                'lat': self.ncfile['lat'][:],
                'lon': self.ncfile['lon'][:],
                #'surge': self.ncfile['surge'][self.WLtime],
                'predictedWL': self.ncfile['predictedWaterLevelHeight'][self.WLdataindex]
                 }

        else:
            print 'ERROR: there is no WATER level Data for this time period!!!'
            self.WLpacket = 0
        return self.WLpacket

    def get_raw_grid(self, output_location, method=0):
        """
        This function is designed to pull the raw gridded text file from the Mobile, AL geospatial data server between
        the times of interest (d1, d2) or the most recent file there in
        method = 0 uses the nearest in time to d1
        method = 1 uses the most recent historical survey but not future to d1
        """
        import download_grid_data as DGD
        # url for raw grid data setup on geospatial database
        grid_url='http://gis.sam.usace.army.mil/server/rest/services/FRF/FRFImportArchive/MapServer/1'
        #query the survey to get the file name and the ID of the file name back for the most recent survey on location
        gridID_list, grid_fname_list, grid_date_list = DGD.query_survey_data(grid_url)
        #
        # do logic here for which survey to pull
        #

        mask = (grid_date_list >= self.epochd1) & (grid_date_list < self.epochd2)  # boolean true/false of time
        maskids = np.where(mask)[0] #where the true values are
        if len(maskids) == 1 :  # there is 1 record found between the dates of interest
            print "One bathymetry surveys found between %s and %s" %(self.d1, self.d2)
            gridID = gridID_list[maskids[0]]
            grid_fname = grid_fname_list[maskids[0]]
        elif len(maskids) < 1 :
            print "No bathymetry surveys found between %s and %s" %(self.d1, self.d2)
            if method == 0:
                idx = np.argmin(np.abs(grid_date_list - self.epochd1))  # closest in time
            # or
            elif method == 1:
                val= (max([n for n in (grid_date_list-self.epochd1) if n<0]))
                idx = np.where((grid_date_list - self.epochd1) == val)[0]

            grid_fname = grid_fname_list[idx]
            gridID = gridID_list[idx]
            gridtime = grid_date_list[idx]
            print "Pulled Bathymetry survey from %s" %grid_fname
        else:
            print ' There Are Multiple Surveys between %s and %s\nPlease Break Simulation up into Multiple Parts.' % (self.d1, self.d2)
            raise
        #
        # download the file name and the ID
        #
        DGD.download_survey(gridID, grid_fname, output_location)
        return grid_fname

    def cliprecords(self, timerecord, recordinterval):
        """
        :param timerecord: the record of the rawdata in datetime format
        :param recordinterval: the interval to chop the data to, starting on the hour
        :return: timeindex - returns the time index of the
        """
        assert isinstance(timerecord[0], DT.datetime), "time record variable must be a datetime instance"
        dt = np.diff(timerecord)
        interval = DT.timedelta(0, recordinterval*60)

        # this code is in development
        # for i in range(0, len(timerecord)):
        #    if
        #       idx = i
        #         break
        # data check at the end
        # assert (np.diff(dtnew)== DT.timedelta(0)).all()
