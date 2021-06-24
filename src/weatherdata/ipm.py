# -*- python -*-
# -*- coding:utf-8 -*-
#
#       Copyright 2020 INRAE-CIRAD
#       Distributed under the Cecill-C License.
#       See https://cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
# ==============================================================================


import pandas as pd
import datetime
import xarray as xr
import numpy as np
import os
import json
import logging
from agroservices import IPM
from weatherdata.settings import pathCache

logging.basicConfig(format='%(levelname)s:%(message)s',encoding='utf-8',level=logging.INFO)

class WeatherDataSource(object):
    ''' 
    Allows to query weather data resource for a given date range and return
    meteorological data in the form of a Python data structure that keeps tracks
    of location and units.

    ..doctest::
        >>> ws = WeatherDataSource(name='Finnish Meteorological Institute measured data')
        >>> ws.station_ids()
        >>> ws.parameters()
        >>> ws.endpoint()
        >>> ws.check_forecast_endpoint()
        >>> ws.data(parameters=[1002,3002], station_id=101104, timeStart='2020-06-12',timeEnd='2020-07-03',timeZone="UTC", altitude=70,longitude=14.3711,latitude=67.2828, ViewDataFrame=True)
    '''
    def __init__(self, name):
        '''
        WeatherDataSource parameters to access at one weather data source of IPM 
        '''
        self.ipm = IPM()
        self.name = name
        self.sources = self.ipm.get_weatherdatasource()
    
    def station_ids(self):
        ''' 
        Get a dataframe with station id and coordinate

        Parameters
        -----------

        Returns
        --------
            a dataframe containing name, id and coordinate of station available for weather resource'''

        values = {item['name']:item['spatial']['geoJSON']for item in self.sources}
        value = values[self.name]
        
        if 'features' in value and value['features']!=[]:
            features = value['features']
            station_id = [feature['properties'] for feature in features]
            coords = [feature['geometry']['coordinates'] for feature in features]
        
            df_stations= pd.DataFrame(station_id)
            
            if len(coords[0])==2:
                df_coords = pd.DataFrame(coords, columns=['latitude','longitude'])
            else:
                df_coords = pd.DataFrame(coords, columns=['latitude','longitude','altitude'])
            df=[df_stations,df_coords]
            data = pd.concat(df, axis=1)
            
        else:
            data = 'no station information for this resource'

        return data

    def parameters(self):
        """
        Get list of available parameters for ressource

        Parameters
        -----------

        Returns
        --------
            a dictionnary containing common and optional parameters
        """
        values = {item['name']:item['parameters']for item in self.sources}
        parameters = values[self.name]

        return parameters

    def endpoint(self):
        """
        Get endpoint associate at the name parameter of WeatherDataSource

        Parameters
        -----------

        Returns
        --------
            a endpoint (str) used in get_data function
        """
        endpoints = self.ipm.weatheradapter_service()

        if self.name in endpoints:
            endpoint = endpoints[self.name]
        
        return endpoint    

    def check_forecast_endpoint(self):
        """
        Check if endpoint is a forecast or not
        
        Parameters
        -----------

        Returns
        --------
            Boolean value True if endpoint is a forecast endpoint either False
        """
        forcast_endpoints=self.ipm.weatheradapter_service(forecast=True).values()
        
        forcast=None
        
        if self.endpoint() in forcast_endpoints:
            forcast=True
        else:
            forcast=False

        return forcast 

    def data(
        self,
        parameters=[1002,3002], 
        stationId=[101104], 
        timeStart='2020-06-12',
        timeEnd='2020-07-03',
        timeZone="UTC",
        altitude=[70],
        longitude=[14.3711],
        latitude=[67.2828],
        format='ds',usecache=True,savecache=True):
        """
        Get weather data from weatherdataressource

        Parameters
        -----------
            parameters: list of parameters of weatherdata 
            station_id: (int) station id of weather station 
            daterange:  a pandas.date_range(start date, end date, freq='H', timeZone(tz))
                        https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.date_range.html
            
            Only for forcast
            ----------------
            altitude: (list) only for Met Norway Locationforecast WGS84 Decimal degrees
            latitude: (list) WGS84 Decimal degrees
            longitude: (list) WGS84 Decimal degrees
        
        Returns
        --------
            return a dataset (format='ds') or json format (format='json') 
        """
        forcast=self.check_forecast_endpoint()

        if forcast==False:
            
            times= pd.date_range(timeStart,timeEnd,freq='H',tz=timeZone)
            
            # time transformation for query format
            timeStart = times[0].strftime('%Y-%m-%dT%H:%M:%S')
            timeEnd = times[-1].strftime('%Y-%m-%dT%H:%M:%S')
            if times.tz._tzname == 'UTC':
                timeStart +='Z'
                timeEnd += 'Z'
            else:
                decstr = times[0].strftime('%z')
                decstr = decstr[:-2] + ':' + decstr[-2:]
                timeStart += decstr
                timeEnd += decstr
            
            interval = pd.Timedelta(times.freq).seconds
            
            
            responses = []
            for station in stationId:
                logging.info('start connecting to station %s' % station)
                try:
                    path=os.path.join(pathCache(),str(station)+'.json')
                    
                    if usecache and os.path.exists(path):
                        with open(path) as f:
                            data=json.load(f)
                    else:
                        data = self.ipm.get_weatheradapter(
                                    endpoint=self.endpoint(),
                                    weatherStationId=station,
                                    timeStart=timeStart,
                                    timeEnd=timeEnd,
                                    interval=interval,
                                    parameters=parameters)
                                    
                        if savecache and type(data) is dict:
                            with open(path,'w') as f:
                                json.dump(data, f)

                    if type(data) is dict:
                        responses.append(data)
                    elif type(data) is int:
                        logging.warn("HTTPError:%s" %data %'for%s' %station)
                    
                except:
                    # log warning 
                    logging.warn("Weather Station not available. %s" %station)
                
        else:
            stationId=None
            if len(latitude)==len(longitude):
                responses = [self.ipm.get_weatheradapter_forecast(
                    endpoint=self.endpoint(), 
                    altitude= altitude[el],
                    latitude=latitude[el],
                    longitude=longitude[el]) for el in range(len(latitude))]
            else:
                raise ValueError("list of latitude and longitude must be have the same length")
            
            #time variable
            times = pd.date_range(
                start=responses[0]['timeStart'], 
                end=responses[0]['timeEnd'], 
                freq="H",
                name="time")


        if format == 'ds':
            #data conversion in numpy array
            datas= [np.array(response['locationWeatherData'][0]['data']) for response in responses]
            dats=[[data[:,i].reshape(data.shape[0],1) for i in range(data.shape[1])] for data in datas]

            # construction of dict for dataset variable
            data_vars=[{str(response['weatherParameters'][i]):(['time','location'],dat[i]) for i in range(len(response['weatherParameters']))} for response in responses for dat in dats]
            
            # construction dictionnaire coordonnée
            if stationId is not None:
                coords=[{'time':times.values,
                'location':([stationId[el]]),
                'lat':[responses[el]['locationWeatherData'][0]['latitude']],
                'lon':[responses[el]['locationWeatherData'][0]['longitude']],
                'alt':[responses[el]['locationWeatherData'][0]['altitude']]} 
                for el in range(len(responses))]
                
            else:
                coords=[{'time':times.values,
                'location':([str([latitude[el],longitude[el]])]),
                'lat':[responses[el]['locationWeatherData'][0]['latitude']],
                'lon':[responses[el]['locationWeatherData'][0]['longitude']],
                'alt':[responses[el]['locationWeatherData'][0]['altitude']]} 
                for el in range(len(responses))]
               
                
            # list de dss
            list_ds=[xr.Dataset(data_vars[el], coords=coords[el]) for el in range(len(responses))]
            #merge ds
            ds=xr.combine_by_coords(list_ds)
            
            #coordinates attributes
            if stationId is not None:
                ds.coords['location'].attrs['name']= 'WeatherStationId'
                ds.coords['lat'].attrs['name']='latitude'
                ds.coords['lat'].attrs['unit']='degrees_north'
                ds.coords['lon'].attrs['name']='longitude'
                ds.coords['lon'].attrs['unit']='degrees_east'
                ds.coords['alt'].attrs['name']='altitude'
                ds.coords['alt'].attrs['unit']='meters'
            else:
                ds.coords['location'].attrs['name']='[latitude,longitude]'
                ds.coords['lat'].attrs['name']='latitude'
                ds.coords['lat'].attrs['unit']='degrees_north'
                ds.coords['lon'].attrs['name']='longitude'
                ds.coords['lon'].attrs['unit']='degrees_east'
                ds.coords['alt'].attrs['name']='altitude'
                ds.coords['alt'].attrs['unit']='meters'                

            #variable attribute
            param = self.ipm.get_parameter()
            p={str(item['id']): item for item in param if item['id'] in responses[0]['weatherParameters']}
            
            for el in list(ds.data_vars):
                ds.data_vars[el].attrs=p[str(el)]
            
            if stationId is not None:
                ds.attrs['weatherRessource']=self.name
                ds.attrs['weatherStationId']=stationId
                ds.attrs['longitude']=list(ds.coords['lon'].values)
                ds.attrs['latitude']=list(ds.coords['lat'].values)
                ds.attrs['timeStart']=ds.coords['time'].values[0]
                ds.attrs['timeEnd']=ds.coords['time'].values[-1]
                ds.attrs['parameters']=list(ds.data_vars)
            else:
                ds.attrs['weatherRessource']=self.name
                ds.attrs['longitude']=list(ds.coords['lon'].values)
                ds.attrs['latitude']=list(ds.coords['lat'].values)
                ds.attrs['timeStart']=ds.coords['time'].values[0]
                ds.attrs['timeEnd']=ds.coords['time'].values[-1]
                ds.attrs['parameters']=list(ds.data_vars)
            
            return ds
        else:
            return responses
                        
       
# TODO : this class should inheritate from a more generic Wheather DataHub
class WeatherDataHub(object):
    """
        Allows to access at IPM weather resources 
        give the list of weather adapter (resources) available on IPM and allows access to weather data source
        
        ..doctest::
        >>> wsh = WeatherDataHub()
        >>> wsh.list_resources()
        >>> wsh.get_resource(name = 'Finnish Meteorological Institute measured data')

    """

    def __init__(self):
        """
            Give an access to IPM interface from agroservice
        """
        self.ipm = IPM()
        self.sources = self.ipm.get_weatherdatasource()

    def list_resources(self):
        """
        get list of ressource available in IPM services

        Parameters:
        -----------

        Returns:
        ---------
            dictionnary with name and description of available weatherdatasource on IPM service
        """
        
        return {item['name']:item['description'] for item in self.sources}
        
    def get_ressource(self, name):
        """
        Parameters:
        -----------
            name: name of weatherdatasource (available in list ressource)
            
        Returns:
        --------
            run weatherdatasource with the name of resource
        """
        keys = [item['name'] for item in self.sources]
        if name in keys:
            return WeatherDataSource(name)
        else:
            raise NotImplementedError("the resource is unknown or the name of the resource is misspelled")
