# -*- python -*-
# -*- coding:utf-8 -*-
#
#       Copyright 2020 INRAE-CIRAD
#       Distributed under the Cecill-C License.
#       See https://cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
# ==============================================================================


import pandas 
import xarray as xr
import numpy as np
import os
import json
import logging

from agroservices import IPM

from weatherdata.settings import pathCache

logging.basicConfig(format='%(levelname)s:%(message)s',level=logging.INFO)

class WeatherDataHub:    
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
        self.sources = None
    
    @property
    def __resources__(self):
        
        if self.sources is None:
            self.sources= self.ipm.get_weatherdatasource()
        
        return {item["name"]:item for item in self.sources}
    
    @property
    def list_resources(self):
        """ display a dataframe of list of resources with their description 

        Returns
        -------
        pandas.DataFrame
            name and description of available weatherdatasource on IPM service
        """   
        df= pandas.DataFrame(self.__resources__).T.reset_index()
        df.rename({"index":"name"},inplace=True)
        
        return df[["name","description","parameters"]]
                     
    
    def __forecast__(self):
        return {key:bool(value["temporal"]["forecast"])for key,value in self.__resources__.items()}
    
    def __endpoint__(self):
        return {key: value["endpoint"] for key, value in self.__resources__.items()}
    
        
    def get_ressource(self, name,df: str):
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
        if name is not None:
            keys = [item for item in self.__resources__]

            if name in keys:
                return WeatherDataSource(name,forecast=self.__forecast__()[name],endpoint=self.__endpoint__()[name], df= None)
            else:
                raise NotImplementedError("the resource is unknown or the name of the resource is misspelled")
        if df is not None:
            name=None
            return WeatherDataSource(name=None,forecast=None,endpoint=None,df=df)
            

class WeatherDataSource(WeatherDataHub):
    def __init__(self, name, forecast,endpoint,df):
        self.name = name
        self.forecast=forecast
        self.endpoint=endpoint
        self.sources=None
        self.ipm = IPM()
        self.df= df
        
  
    @property
    def __source__(self):
        
        if self.sources is None:
            self.sources=self.__resources__
            
        source= self.sources[self.name]
        return source
          
    
    @property               
    def parameter(self):
        parameter= self.__source__["parameters"]
        return parameter
    
    @property
    def stations(self):
        if self.__source__["spatial"]["geoJSON"] is not None:
            features=json.loads(self.__source__["spatial"]["geoJSON"])['features']
            
            #recupère les infos stations dans une properties
            stations=[feature["properties"] for feature in features]
            
            #recuperation et transformation des coordonnées
            coord_tmp=[feature['geometry']['coordinates'] for feature in features]
            station_coords= [{"latitude":float(coord[0]), "longitude":float(coord[1])} for coord in coord_tmp]
            
            # ajoute les coordonnées dans stations
            for el in range(len(stations)):
                stations[el].update(station_coords[el])
            
            # affichage des stations comme dataframe    
            df= pandas.DataFrame(stations)
            return df
        else:
            print("No stations informations for this ressources")
        
    def data(self,
             parameters =[1002,3002], 
             stationId =[101104], 
             timeStart = '2020-06-12',
             timeEnd = '2020-07-03',
             timeZone = "UTC",
             altitude = [70.0],
             longitude = [14.3711],
             latitude = [67.2828],
             credentials = None,
             interval = 3600,
             display ='ds',
             varname = 'id',
             usecache =False,
            savecache =False):
        
        responses=[] 
        
        if self.forecast== False: 
            times= pandas.date_range(timeStart,timeEnd,freq=str(interval)+'s',tz=timeZone)

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

            interval = pandas.Timedelta(times.freq).seconds
                
            for station in stationId:
                logging.info('start connecting to station %s' % station)
                path=os.path.join(pathCache(),str(station)+'_'+str(parameters)+"_"+timeStart.split("T")[0]+"_"+timeEnd.split("T")[0]+'.json')
                
                
                if usecache and os.path.exists(path):
                    with open(path) as f:
                        data=json.load(f)
                else:        
                    data = self.ipm.get_weatheradapter(
                                    endpoint=self.endpoint,
                                    weatherStationId=station,
                                    timeStart=timeStart,
                                    timeEnd=timeEnd,
                                    interval=interval,
                                    parameters=parameters,
                                    credentials= credentials)
                    
                
                if type(data) is dict:
                    responses.append(data)
                elif type(data) is int:
                    logging.warning('HTTPError: %s for %s' %(data,station))   
                
                if savecache and type(data) is dict:
                    with open(path,'w') as f:
                        json.dump(data, f)  
                
        elif self.endpoint in ["https://ipmdecisions.nibio.no/api/wx/rest/weatheradapter/dmipoint/",'https://ipmdecisions.nibio.no/api/wx/rest/weatheradapter/lantmet/']:
            stationId=None
            
            times= pandas.date_range(timeStart,timeEnd,freq=str(interval)+'S',tz=timeZone)

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
                
            for el in range(len(latitude)):
                path=os.path.join(pathCache(),str(timeStart)+'_'+str(timeEnd)+'_'+str(parameters)+str(altitude[el])+'_'+str(latitude[el])+"_"+str(longitude[el])+'.json')
            
                if usecache and os.path.exists(path):
                    with open(path) as f:
                        data=json.load(f)
                else:
                    data= self.ipm.get_weatheradapter_forecast(
                        endpoint=self.endpoint, 
                        altitude= altitude[el],
                        latitude=latitude[el],
                        longitude=longitude[el],
                        timeStart=timeStart,
                        timeEnd=timeEnd,
                        interval=interval,
                        parameters = parameters
                        )

                if type(data) is dict:
                    responses.append(data)
                elif type(data) is int:
                    logging.warning("HTTPError:%s for %s" %(data,[altitude[el],latitude[el],longitude[el]]))
                
                if savecache and type(data) is dict:
                    with open(path,'w') as f:
                        json.dump(data, f)
        else:
            stationId=None
            timeStart==None
            timeEnd==None
            interval=None
            for el in range(len(latitude)):
                path=os.path.join(pathCache(),str(altitude[el])+'_'+str(latitude[el])+"_"+str(longitude[el])+'.json')
            
                if usecache and os.path.exists(path):
                    with open(path) as f:
                        data=json.load(f)
                else:
                    data= self.ipm.get_weatheradapter_forecast(
                        endpoint=self.endpoint, 
                        altitude= altitude[el],
                        latitude=latitude[el],
                        longitude=longitude[el])

                if type(data) is dict:
                    responses.append(data)
                elif type(data) is int:
                    logging.warning("HTTPError:%s for %s" %(data,[altitude[el],latitude[el],longitude[el]]))
                
                if savecache and type(data) is dict:
                    with open(path,'w') as f:
                        json.dump(data, f)
        
        if display=="ds":
            return self.__convert_xarray_dataset__(responses,stationId,varname,display)
        else:
            return responses
    
    def __convert_xarray_dataset__(self, responses,stationId,varname,display):
        
        if display != "ds":
            return responses
        else:          
            times=pandas.date_range(start=responses[0]["timeStart"],
                                    end=responses[0]["timeEnd"],
                                    freq=str(responses[0]["interval"])+"S",
                                    name="time")
            
            #times.strftime('%Y-%m-%dT%H:%M:%S')
            
            datas= [np.array(response['locationWeatherData'][0]['data']).astype("float") for response in responses]
            
            dats = [[data[:,i].reshape(data.shape[0],1) for i in range(data.shape[1])] for data in datas]
            

            # construction of dict for dataset variable
            data_vars=[{str(response['weatherParameters'][i]):(['time','location'],dat[i]) for i in range(len(response['weatherParameters']))} for response in responses for dat in dats]

            # construction dictionnaire coordonnée
            if stationId:
                coords=[{'time':times.values,
                'location':([stationId[el]]),
                'lat':("location",[float(responses[el]['locationWeatherData'][0]['latitude'])]),
                'lon':("location",[float(responses[el]['locationWeatherData'][0]['longitude'])]),
                #'alt':[float(responses[el]['locationWeatherData'][0]['altitude'])]
                } 
                for el in range(len(responses))]
                
            else:
                coords=[{'time':times.values,
                        'location':([str([responses[el]['locationWeatherData'][0]['latitude'],responses[el]['locationWeatherData'][0]['longitude']])]),
                        'lat':('location',[responses[el]['locationWeatherData'][0]['latitude']]),
                        'lon':('location',[responses[el]['locationWeatherData'][0]['longitude']]),
            #'alt':[float(responses[el]['locationWeatherData'][0]['altitude'])]
            } for el in range(len(responses))]
                
                    
            # list de ds
            list_ds=[xr.Dataset(data_vars[el], coords=coords[el]) for el in range(len(responses))]
            
            #merge ds
            ds=xr.merge(list_ds)
            
            #add coordinates attributes
            if stationId:
                ds.coords['time'].attrs["name"]="time"
                ds.coords['location'].attrs['name']= 'WeatherStationId'
                ds.coords['lat'].attrs['name']='latitude'
                ds.coords['lat'].attrs['unit']='degrees_north'
                ds.coords['lon'].attrs['name']='longitude'
                ds.coords['lon'].attrs['unit']='degrees_east'
            else:
                #ds.coords['location'].attrs['name']='[latitude,longitude]'
                ds.coords['lat'].attrs['name']='latitude'
                ds.coords['lat'].attrs['unit']='degrees_north'
                ds.coords['lon'].attrs['name']='longitude'
                ds.coords['lon'].attrs['unit']='degrees_east'
            
            # add data variable  attributes
            param = self.ipm.get_parameter()
            p={str(item['id']): item for item in param if item['id'] in responses[0]['weatherParameters']}
                    
                
            for el in list(ds.data_vars):
                try:
                    ds.data_vars[el].attrs=p[str(el)]
                except KeyError as e:
                    logging.exception("The weatherParameter not implemented; key error: %s".format(e))
            
            # Attribute of dataset
            if stationId:
                ds.attrs['weatherRessource']=self.name
                #ds.attrs['weatherStationId']=stationId
                ds.attrs['timeStart']=str(ds.coords['time'].values[0])
                ds.attrs['timeEnd']=str(ds.coords['time'].values[-1])
                ds.attrs['parameters']=list(ds.data_vars)
            else:
                ds.attrs['weatherRessource']=self.name
                ds.attrs['timeStart']=str(ds.coords['time'].values[0])
                ds.attrs['timeEnd']=str(ds.coords['time'].values[-1])
                ds.attrs['parameters']=list(ds.data_vars)
            
            if varname=="name":
                ds= ds.rename_vars(name_dict={str(ds[el].attrs['id']):ds[el].attrs['name'] for el in list(ds.keys())}) 
                
        return ds
    
    def dataframe_to_ipm(self,longitude=3.87, 
                       latitude=43.61,
                       altitude=0.0,
                       timezone="Europe/Paris",
                       interval=3600,
                       convert_name={'temperature_air':1002,
                                     "relative_humidity":3001,
                                     "rain":2001,
                                     "wind_speed":4005,
                                     "global_radiation":5001},
                       display="json"):
        """Convert weather dataframe into IPM weather output schema

        Parameters
        ----------
        longitude : float, optional
            longitudinal coordinate in degree of the weather dataframe, by default 3.87
        latitude : float, optional
            latitude coordinate in degree of the weather dataframe  , by default 43.61
        altitude : float, optional
            altitude coordinate in degree of the weather dataframe, by default 0.0
        timezone : str, optional
            time zone of dataframe eg. Europe/Paris if weatherdata is in france, by default "Europe/Paris"
        interval : int, optional
            interval time between index in second eg 3600 if weather data is in hour , by default 3600
        convert_name : dict, optional
            dict of conversion between weather dataframe and ipm parameters, by default {'temperature_air':1002, "relative_humidity":3001, "rain":2001, "wind_speed":4005, "global_radiation":5001}
        display : str, optional
            choose the type of data according json schema ipm or ds in xarray.dataset , by default "json"

        Returns
        -------
        json or xarray.dataset
            return data in weatherdata according to ipm input (json) or in xarray.dataset (ds)
        """
        
        
        data=self.df
        data=data.rename(columns=convert_name)
        time=pandas.date_range(start=data.index[0],end=data.index[-1],tz="Europe/Paris",freq=str(interval)+"s").tz_convert("UTC").strftime('%Y-%m-%dT%H:%M:%S')+"Z"
        
        weather_ipm_schema={}
        weather_ipm_schema["timeStart"]=time.tolist()[0]
        weather_ipm_schema["timeEnd"]=time.tolist()[-1]
        weather_ipm_schema["interval"]=interval
        weather_ipm_schema['weatherParameters']=data.columns.to_list()
        weather_ipm_schema["locationWeatherData"]=[
            {"longitude":longitude,
            "latitude":latitude,
            "altitude":altitude,
            "amalgamation":np.repeat(0,data.shape[1]).tolist(),
            "data":np.array(data).tolist(),
            "qc":np.repeat(0,data.shape[1]).tolist(),
            "width":data.shape[1],
            "length":data.shape[0]}
        ]
        
        if display=="ds":
            return self.__convert_xarray_dataset__([weather_ipm_schema],stationId=None,varname="id",display="ds")
        else:
            responses=weather_ipm_schema
        return [responses]