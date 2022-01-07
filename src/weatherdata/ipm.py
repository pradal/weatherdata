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
from typing import Union, List
from agroservices import IPM

from weatherdata.settings import pathCache

logging.basicConfig(format='%(levelname)s:%(message)s',level=logging.INFO)

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
        """[summary]

        Parameters
        ----------
        name : str
            name of the IPM WeatherDataSource
        """        
        self.ipm = IPM()
        self.name = name
        self.sources = self.ipm.get_weatherdatasource()
    
    def station_ids(self)->pd.DataFrame:
        """Get a dataframe with station id and coordinate

        Returns
        -------
        pd.DataFrame
            dataframe containing name, id and coordinate of station available for weather resource
        """          
        values = {item['name']:item['spatial']['geoJSON']for item in self.sources}
        value = json.loads(values[self.name])
        
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

    def parameters(self) -> dict:      
        """ Get list of available parameters for ressource

        Returns
        -------
        dict
            a dictionnary containing common and optional parameters
        """

        values = {item['name']:item['parameters']for item in self.sources}
        parameters = values[self.name]

        return parameters

    def endpoint(self) -> str:
        """Get endpoint associate at WeatherDataSource

        Returns
        -------
        str
            a endpoint of WeatherDataSource
        """        
        endpoints = self.ipm.weatheradapter_service()

        if self.name in endpoints:
            endpoint = endpoints[self.name]
        
        return endpoint    

    def check_forecast_endpoint(self) -> bool:
        """Check if endpoint is a forecast or not

        Returns
        -------
        bool
            True if endpoint is a forecast endpoint either False
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
        parameters: List[int]=[1002,3002], 
        stationId: List[int]=[101104], 
        timeStart: str = '2020-06-12',
        timeEnd: str = '2020-07-03',
        timeZone: str = "UTC",
        altitude: List[Union[int,float]] = [70.0],
        longitude: List[Union[int,float]] = [14.3711],
        latitude: List[Union[int,float]] = [67.2828],
        credentials: dict = None,
        interval: int = 3600,
        format: str ='ds',
        varname:str = 'id',
        usecache: bool=False,
        savecache: bool=False) -> Union[xr.Dataset,List[dict]]:
        
        """ Get weather data from WeatherDataSource

        Parameters
        ----------
        parameters : list[int], 
            weatherdata parameters, by default [1002,3002]
        stationId : list[int],
            id of the station, by default [101104]
        timeStart : str, 
            start date of weather, by default '2020-06-12'
        timeEnd : str, 
            end date of weather, by default '2020-07-03'
        timeZone : str,
            time zone of weather, by default "UTC"
        
        Only for forecast data:
        altitude : list[Union[int,float]], 
            only for Met Norway Locationforecast WGS84 Decimal degrees, by default [70.0]
        longitude : list[Union[int,float]], 
            WGS84 Decimal degrees, by default [14.3711]
        latitude : list[Union[int,float]], 
            WGS84 Decimal degrees, by default [67.2828]
        format : str, 
            type of output xarray.dataset or json, by default 'ds'
        usecache : bool, 
            use cache directory or not, by default True
        savecache : bool,
            save in cache directory or not, by default True

        Returns
        -------
        Union[xr.dataset,list[dict]]
            Weather data output according to query

        Raises
        ------
        ValueError
            len(latitude) = len(altitude)
        """        
        forcast=self.check_forecast_endpoint()

        if forcast==False:
            
            interval=interval

            responses = []
            for station in stationId:
                logging.info('start connecting to station %s' % station)

            
                path=os.path.join(pathCache(),str(station)+'_'+str(parameters)+"_"+timeStart.split("T")[0]+"_"+timeEnd.split("T")[0]+'.json')
                
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
                                parameters=parameters,
                                credentials= credentials)
                                
                if type(data) is dict:
                    responses.append(data)
                elif type(data) is int:
                    logging.warning('HTTPError:%s' %data %'for%s' %station)

                if savecache and type(data) is dict:
                    with open(path,'w') as f:
                        json.dump(data, f)
                    
        else:
            stationId=None
            responses=[]
            
            for el in range(len(latitude)):
                path=os.path.join(pathCache(),str(altitude[el])+'_'+str(latitude[el])+"_"+str(longitude[el])+'.json')
            
                if usecache and os.path.exists(path):
                    with open(path) as f:
                        data=json.load(f)
                else:
                    data= self.ipm.get_weatheradapter_forecast(
                        endpoint=self.endpoint(), 
                        altitude= altitude[el],
                        latitude=latitude[el],
                        longitude=longitude[el])

                if type(data) is dict:
                    responses.append(data)
                elif type(data) is int:
                    logging.warning("HTTPError:%s" %data %'for%s' %[altitude[el],latitude[el],longitude[el]])
                
                if savecache and type(data) is dict:
                    with open(path,'w') as f:
                        json.dump(data, f)
        
        #time variable
        times = pd.date_range(
            start=responses[0]['timeStart'], 
            end=responses[0]['timeEnd'], 
            freq="H",
            name="time")
        
        times.strftime('%Y-%m-%dT%H:%M:%S')



        if format == 'ds':
            #data conversion in numpy array
            datas= [np.array(response['locationWeatherData'][0]['data']) for response in responses]
            dats = [[data[:,i].reshape(data.shape[0],1) for i in range(data.shape[1])] for data in datas]

            # construction of dict for dataset variable
            data_vars=[{str(response['weatherParameters'][i]):(['time','location'],dat[i]) for i in range(len(response['weatherParameters']))} for response in responses for dat in dats]
            
            # construction dictionnaire coordonnée
            if stationId:
                coords=[{'time':times.values,
                'location':([stationId[el]]),
                'lat':[float(responses[el]['locationWeatherData'][0]['latitude'])],
                'lon':[float(responses[el]['locationWeatherData'][0]['longitude'])],
                'alt':[float(responses[el]['locationWeatherData'][0]['altitude'])]} 
                for el in range(len(responses))]
                
            else:
                coords=[{'time':times.values,
                'location':([str([latitude[el],longitude[el]])]),
                'lat':[float(responses[el]['locationWeatherData'][0]['latitude'])],
                'lon':[float(responses[el]['locationWeatherData'][0]['longitude'])],
                'alt':[float(responses[el]['locationWeatherData'][0]['altitude'])]} 
                for el in range(len(responses))]
               
                
            # list de ds
            list_ds=[xr.Dataset(data_vars[el], coords=coords[el]) for el in range(len(responses))]
            
            #merge ds
            ds=xr.combine_by_coords(list_ds)

            #coordinates attributes
            if stationId:
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
                try:
                    ds.data_vars[el].attrs=p[str(el)]
                except KeyError as e:
                    logging.exception("The weatherParameter not implemented; key error: %s".format(e))

            if varname == 'name': 
                ds= ds.rename_vars(name_dict={str(ds[el].attrs['id']):ds[el].attrs['name'] for el in list(ds.keys())})
            
            if stationId:
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

    def list_resources(self)->dict:
        """ Get list of ressource available in IPM services

        Returns
        -------
        dict
            name and description of available weatherdatasource on IPM service
        """                
       
        return {item['name']:item['description'] for item in self.sources}
        
    def get_ressource(self, name: str)-> WeatherDataSource:
        """ Get ressource from WeatherDataSource

        Parameters
        ----------
        name : str
             name of weatherdatasource (available in list ressource)

        Returns
        -------
        WeatherDataSource
           weatherdatasource with the name of resource

        Raises
        ------
        NotImplementedError
            the resource is unknown or the name of the resource is misspelled
        """        
        keys = [item['name'] for item in self.sources]

        if name in keys:
            return WeatherDataSource(name)
        else:
            raise NotImplementedError("the resource is unknown or the name of the resource is misspelled")

