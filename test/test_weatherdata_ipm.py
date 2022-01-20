import pandas
import xarray
import numpy
from weatherdata.ipm import WeatherDataHub, WeatherDataSource

wdh= WeatherDataHub()
list_resources = list(wdh.list_resources())

def keys_exists(dict_, keys, test = all):
    return test(key in dict_ for key in keys)

def testListRessource():
    '''
    Test list_ressource function
    '''
    rep= wdh.list_resources()
    assert type(rep) is dict, rep
    assert keys_exists(
            rep.keys(),
            ('Met Norway Locationforecast', 
            'FMI weather forecasts', 
            'Finnish Meteorological Institute measured data', 
            'Landbruksmeteorologisk tjeneste', 'MeteoBot API',
            'Fruitweb',
            'Metos')
        )

def testGetRessource():
    '''
    Test get resource functoin for all ressources
    '''

    for name in list_resources:
        rep=wdh.get_ressource(name=name)
        if isinstance(rep,WeatherDataSource):
            pass

def testStationId():
    '''
    Test station_id function for all ressources
    '''
    wds_station_ids={name:WeatherDataSource(name=name).station_ids() for name in list_resources}

    # Met Norway Locationforecast resource
    assert type(wds_station_ids['Met Norway Locationforecast']) is str
    assert wds_station_ids['Met Norway Locationforecast'] == 'no station information for this resource'
    #Deutsche Wetterdienst location forecast by IPM Decisions
    # FMI weather forecasts resource
    assert type(wds_station_ids['FMI weather forecasts']) is str
    assert wds_station_ids['FMI weather forecasts'] == 'no station information for this resource'

    # Finnish Meteorological Institute measured data resource
    assert type(wds_station_ids['Finnish Meteorological Institute measured data']) is pandas.DataFrame
    assert wds_station_ids['Finnish Meteorological Institute measured data'].shape==(208,4)
    assert list(wds_station_ids['Finnish Meteorological Institute measured data'].columns)==['name', 'id', 'latitude','longitude']
    # Landbruksmeteorologisk tjeneste resource
    assert type(wds_station_ids['Landbruksmeteorologisk tjeneste']) is pandas.DataFrame
    assert wds_station_ids['Landbruksmeteorologisk tjeneste'].shape==(92,6)
    assert list(wds_station_ids['Landbruksmeteorologisk tjeneste'].columns)==["name","id","WMOCertified","latitude","longitude","altitude"]
    # MeteoBot API resource
    assert type(wds_station_ids['MeteoBot API']) is pandas.DataFrame
    assert wds_station_ids['MeteoBot API'].shape==(528,4)
    assert list(wds_station_ids['MeteoBot API'].columns)==['name', 'id', 'latitude','longitude']
    # Fruitweb resource
    assert type(wds_station_ids['Fruitweb']) is str
    assert wds_station_ids['Fruitweb'] == 'no station information for this resource'

    # Metos resource
    assert type(wds_station_ids['Metos']) is str
    assert wds_station_ids['Fruitweb'] == 'no station information for this resource'

def testParameters():
    '''
    Test parameters function for all resources
    '''
    wds_parameters={name:WeatherDataSource(name=name).parameters() for name in list_resources}

    # Met Norway Locationforecast resource
    assert type(wds_parameters['Met Norway Locationforecast']) is dict
    assert type(wds_parameters['Met Norway Locationforecast']['common']) is list
    assert wds_parameters['Met Norway Locationforecast']['common'] == [1001, 3001, 2001, 4002]
    assert wds_parameters['Met Norway Locationforecast']['optional'] is None
    # FMI weather forecasts resource
    assert type(wds_parameters['FMI weather forecasts']) is dict
    assert type(wds_parameters['FMI weather forecasts']['common']) is list
    assert wds_parameters['FMI weather forecasts']['common'] == [1001, 1901, 2001, 3001, 4002, 5001]
    assert wds_parameters['FMI weather forecasts']['optional'] is None

    # Finnish Meteorological Institute measured data resource
    assert type(wds_parameters['Finnish Meteorological Institute measured data']) is dict
    assert type(wds_parameters['Finnish Meteorological Institute measured data']['common']) is list
    assert wds_parameters['Finnish Meteorological Institute measured data']['common'] == [1002, 3002, 2001, 4003]
    assert wds_parameters['Finnish Meteorological Institute measured data']['optional'] is None
    # Landbruksmeteorologisk tjeneste resource
    assert type(wds_parameters['Landbruksmeteorologisk tjeneste']) is dict
    assert type(wds_parameters['Landbruksmeteorologisk tjeneste']['common']) is list
    assert wds_parameters['Landbruksmeteorologisk tjeneste']['common'] == [1002, 1003, 1004, 3002, 2001, 4003]
    assert wds_parameters['Landbruksmeteorologisk tjeneste']['optional'] == [3101, 5001]

    # MeteoBot API resource
    assert type(wds_parameters['MeteoBot API']) is dict
    assert type(wds_parameters['MeteoBot API']['common']) is list
    assert wds_parameters['MeteoBot API']['common'] == [1001, 3001, 2001, 4002]
    assert wds_parameters['MeteoBot API']['optional'] is None
    
    # Fruitweb resource
    assert type(wds_parameters['Fruitweb']) is dict
    assert type(wds_parameters['Fruitweb']['common']) is list
    assert wds_parameters['Fruitweb']['common'] == [1001, 3001, 2001, 4002] 
    assert wds_parameters['Fruitweb']['optional'] is None

    # Metos resource
    assert type(wds_parameters['Metos']) is dict
    assert type(wds_parameters['Metos']['common']) is list
    assert wds_parameters['Metos']['common'] == [1001, 3001, 2001, 4002] 
    assert wds_parameters['Metos']['optional'] is None

def testEndpoint():
    '''
    Test endpoint function for all ressources
    '''
    wds_endpoints={name:WeatherDataSource(name=name).endpoint() for name in list_resources}

    # Met Norway Locationforecast resource
    assert type(wds_endpoints['Met Norway Locationforecast']) is str
    assert wds_endpoints['Met Norway Locationforecast']== 'https://ipmdecisions.nibio.no/api/wx/rest/weatheradapter/yr/'

    # FMI weather forecasts resource
    assert type(wds_endpoints['FMI weather forecasts']) is str
    assert wds_endpoints['FMI weather forecasts']== 'https://ipmdecisions.nibio.no/api/wx/rest/weatheradapter/fmi/forecasts'

    # Finnish Meteorological Institute measured data resource
    assert type(wds_endpoints['Finnish Meteorological Institute measured data']) is str
    assert wds_endpoints['Finnish Meteorological Institute measured data']== 'https://ipmdecisions.nibio.no/api/wx/rest/weatheradapter/fmi/'

    # Landbruksmeteorologisk tjeneste resource
    assert type(wds_endpoints['Landbruksmeteorologisk tjeneste']) is str
    assert wds_endpoints['Landbruksmeteorologisk tjeneste']== 'https://lmt.nibio.no/services/rest/ipmdecisions/getdata/'

    # MeteoBot API resource
    assert type(wds_endpoints['MeteoBot API']) is str
    assert wds_endpoints['MeteoBot API']== 'https://ipmdecisions.nibio.no/api/wx/rest/weatheradapter/meteobot/'

    # Fruitweb resource
    assert type(wds_endpoints['Fruitweb']) is str
    assert wds_endpoints['Fruitweb']== 'https://ipmdecisions.nibio.no/api/wx/rest/weatheradapter/davisfruitweb/'

    # Metos resource
    assert type(wds_endpoints['Metos']) is str
    assert wds_endpoints['Metos']== 'https://ipmdecisions.nibio.no/api/wx/rest/weatheradapter/metos/'

def testCheckForcast():
    '''
    Test check_forcast function for all ressources
    '''
    wds_check_forcast={name:WeatherDataSource(name=name).check_forecast_endpoint() for name in list_resources}

    # Met Norway Locationforecast resource
    assert type(wds_check_forcast['Met Norway Locationforecast']) is bool
    assert wds_check_forcast['Met Norway Locationforecast'] is True

    # FMI weather forecasts resource
    assert type(wds_check_forcast['FMI weather forecasts']) is bool
    assert wds_check_forcast['FMI weather forecasts'] is True

    # Finnish Meteorological Institute measured data resource
    assert type(wds_check_forcast['Finnish Meteorological Institute measured data']) is bool
    assert wds_check_forcast['Finnish Meteorological Institute measured data'] is False

    # Landbruksmeteorologisk tjeneste resource
    assert type(wds_check_forcast['Landbruksmeteorologisk tjeneste']) is bool
    assert wds_check_forcast['Landbruksmeteorologisk tjeneste'] is False

    # MeteoBot API resource
    assert type(wds_check_forcast['MeteoBot API']) is bool
    assert wds_check_forcast['MeteoBot API'] is False

    # Fruitweb resource
    assert type(wds_check_forcast['Fruitweb']) is bool
    assert wds_check_forcast['Fruitweb'] is False

    # Metos resource
    assert type(wds_check_forcast['Metos']) is bool
    assert wds_check_forcast['Metos'] is False

# test for one argument
#Test for one stations
def testDataStationMetNorway():
    '''
    Test Met_Norway data function

    Params:
    -------
        latitude:(list) [67.2828]
        longitude: (list) [14.3711]
        altitude:(list) [70]
    '''
    
    # Met Norway Locationforecast resource
    ## test ds format
    norway=WeatherDataSource(name='Met Norway Locationforecast')
    rep_ds=norway.data(latitude=[67.2828],longitude=[14.3711],altitude=[70],format="ds")
    assert type(rep_ds) is xarray.Dataset
    assert keys_exists(dict(rep_ds.dims),('alt','lat','location','lon','time'))
    
    ### test coords
    assert list(rep_ds.coords)==['time', 'location', 'lat', 'lon', 'alt']
    assert rep_ds.coords['time'].dtype=='<M8[ns]'
    assert rep_ds.coords['time'].attrs=={}
    assert rep_ds.coords['location'].dtype=='<U18'
    assert rep_ds.coords['location'].values=='[67.2828, 14.3711]'
    assert rep_ds.coords['location'].attrs=={'name': '[latitude,longitude]'}
    assert rep_ds.coords['lat'].dtype=='float64'
    assert rep_ds.coords['lat'].attrs=={'name': 'latitude', 'unit': 'degrees_north'}
    assert rep_ds.coords['lat'].values==[67.2828]
    assert rep_ds.coords['lon'].dtype=='float64'
    assert rep_ds.coords['lon'].attrs=={'name': 'longitude', 'unit': 'degrees_east'}
    assert rep_ds.coords['lon'].values==[14.3711]
    assert rep_ds.coords['alt'].dtype=='float64'
    assert rep_ds.coords['alt'].attrs=={'name': 'altitude', 'unit': 'meters'}
    assert rep_ds.coords['alt'].values==[70]
    
    ### test data variable
    assert list(rep_ds.data_vars) == ['1001', '3001', '2001', '4002']
    assert rep_ds.data_vars['1001'].dtype == 'float64'
    assert rep_ds.data_vars['1001'].attrs == {'id': 1001, 'name': 'Instantaneous temperature at 2m', 'description': None, 'unit': 'Celcius'}    
    assert rep_ds.data_vars['3001'].dtype == 'float64'
    assert rep_ds.data_vars['3001'].attrs == {'id': 3001, 'name': 'Instantaneous RH at 2m (%)', 'description': None, 'unit': '%'}    
    assert rep_ds.data_vars['2001'].dtype == 'float64'
    assert rep_ds.data_vars['2001'].attrs == {'id': 2001, 'name': 'Precipitation', 'description': None, 'unit': 'mm'}
    assert rep_ds.data_vars['4002'].dtype == 'float64'
    assert rep_ds.data_vars['4002'].attrs == {'id': 4002, 'name': 'Instantaneous wind speed at 2m', 'description': None, 'unit': 'm/s'}

    ### test ds attribute
    assert type(rep_ds.attrs) is dict
    assert keys_exists(rep_ds.attrs,('weatherRessource','longitude','latitude','timeStart','timeEnd','parameters'))
    assert rep_ds.attrs['weatherRessource']=='Met Norway Locationforecast'
    assert rep_ds.attrs['longitude']==[14.3711]
    assert rep_ds.attrs['latitude']==[67.2828]
    assert rep_ds.attrs['parameters']==['1001', '3001', '2001', '4002']

    ###test conversion dataframe
    assert rep_ds.to_dataframe().shape[1]==4
    assert rep_ds.to_dataframe().index.names==['alt', 'lat', 'location', 'lon', 'time']

    # format= json
    rep_json=norway.data(latitude=[67.2828],longitude=[14.3711],altitude=[70],format="json")
    assert type(rep_json[0]) is dict
    assert keys_exists(rep_json[0],('timeStart', 'timeEnd', 'interval', 'weatherParameters', 'locationWeatherData'))
    assert rep_json[0]['weatherParameters']==[1001, 3001, 2001, 4002]
    assert rep_json[0]['locationWeatherData'][0]['longitude']==14.3711
    assert rep_json[0]['locationWeatherData'][0]['latitude']==67.2828
    assert rep_json[0]['locationWeatherData'][0]['altitude']==70

def testDataStationFMIForecasts():
    '''
    Test 'FMI weather forecasts' data function for one parameter by argument

    Params:
    -------
        latitude:(list) [67.2828]
        longitude: (list) [14.3711]
        altitude:(list) [70]
    
    Problem: parameter 1901 is not in get.parameter()
    -------
    '''
    
    ## test ds format
    fmi_forecasts=WeatherDataSource(name='FMI weather forecasts')
    rep_ds=fmi_forecasts.data(latitude=[67.2828],longitude=[14.3711],altitude=[70],format="ds")
    assert type(rep_ds) is xarray.Dataset
    assert keys_exists(dict(rep_ds.dims),('alt','lat','location','lon','time'))

def testDataStationFMI():
    '''
    Test 'Finnish Meteorological Institute measured data' data function for one parameter by argument

    Params:
    -------
        stationId= [101104]
        parameters = [1002,3002]
        timeStart = '2020-06-12'
        timeEnd = '2020-07-03'
        timeZone = 'UTC'

    '''
    
    ## test ds format
    fmi=WeatherDataSource(name='Finnish Meteorological Institute measured data')
    rep_ds=fmi.data(
        stationId=[101104],
        parameters=[1002,3002],
        timeStart = '2020-06-12',
        timeEnd = '2020-07-03',
        timeZone='UTC',
        format="ds")
    assert type(rep_ds) is xarray.Dataset
    assert keys_exists(dict(rep_ds.dims),('alt','lat','location','lon','time'))

    ### test coords
    assert list(rep_ds.coords)==['time', 'location', 'lat', 'lon', 'alt']
    assert rep_ds.coords['time'].dtype=='<M8[ns]'
    assert rep_ds.coords['time'].attrs=={}
    assert rep_ds.coords['location'].dtype=='int32'
    assert rep_ds.coords['location'].values==[101104]
    assert rep_ds.coords['lat'].dtype=='float64'
    assert rep_ds.coords['lat'].attrs=={'name': 'latitude', 'unit': 'degrees_north'}
    assert rep_ds.coords['lat'].values==[60.81397]
    assert rep_ds.coords['lon'].dtype=='float64'
    assert rep_ds.coords['lon'].attrs=={'name': 'longitude', 'unit': 'degrees_east'}
    assert rep_ds.coords['lon'].values==[23.49825]
    assert rep_ds.coords['alt'].dtype=='float64'
    assert rep_ds.coords['alt'].attrs=={'name': 'altitude', 'unit': 'meters'}
    assert rep_ds.coords['alt'].values==[0.]
    
    ### test data variable
    assert list(rep_ds.data_vars) == ['1002', '3002']
    assert rep_ds.data_vars['1002'].dtype == 'float64'
    assert rep_ds.data_vars['1002'].attrs == {'id': 1002, 'name': 'Mean air temperature at 2m', 'description': None, 'unit': 'Celcius'}    
    assert rep_ds.data_vars['3002'].dtype == 'float64'
    assert rep_ds.data_vars['3002'].attrs == {'id': 3002, 'name': 'Mean RH at 2m', 'description': None, 'unit': '%'}    

    ### test ds attribute
    assert type(rep_ds.attrs) is dict
    assert keys_exists(rep_ds.attrs,('weatherRessource','longitude','latitude','timeStart','timeEnd','parameters'))
    assert rep_ds.attrs['weatherRessource']=='Finnish Meteorological Institute measured data'
    assert rep_ds.attrs['longitude']==[23.49825]
    assert rep_ds.attrs['latitude']==[60.81397]
    assert rep_ds.attrs['parameters']==['1002', '3002']

    ###test conversion dataframe
    assert rep_ds.to_dataframe().shape[1]==2
    assert rep_ds.to_dataframe().index.names==['alt', 'lat', 'location', 'lon', 'time']

    # format= json
    rep_json=fmi.data(
        stationId=[101104],
        parameters=[1002,3002],
        timeStart = '2020-06-12',
        timeEnd = '2020-07-03',
        timeZone='UTC',
        format="json")
    assert type(rep_json[0]) is dict
    assert keys_exists(rep_json[0],('timeStart', 'timeEnd', 'interval', 'weatherParameters', 'locationWeatherData'))
    assert rep_json[0]['weatherParameters']==[1002, 3002]
    assert rep_json[0]['locationWeatherData'][0]['longitude']==23.49825
    assert rep_json[0]['locationWeatherData'][0]['latitude']==60.81397
    assert rep_json[0]['locationWeatherData'][0]['altitude']==0.0

def testDataStationLandbruks():
    '''
    Test 'Landbruksmeteorologisk tjeneste' data function for one parameter by argument

    Params:
    -------
        stationId= 46
        parameters = [1002,3002]
        timeStart = '2020-06-12'
        timeEnd = '2020-07-03'
        timeZone = 'UTC'
    
    Problem: responses is empty this endpoint are not available problem with location

    '''
    
    ## test ds format
    land=WeatherDataSource(name='Landbruksmeteorologisk tjeneste')
    rep_ds=land.data(
        stationId=[46],
        parameters=[1002,3002],
        timeStart = '2020-06-12',
        timeEnd = '2020-07-03',
        timeZone='UTC',
        format="ds")
    assert type(rep_ds) is xarray.Dataset
    assert keys_exists(dict(rep_ds.dims),('alt','lat','location','lon','time'))

# test for a list of argument
def testDataStationsMetNorway():
    '''
    Test Met_Norway data function

    Params:
    -------
        latitude:(list) [67.2828, 68.3737]
        longitude: (list) [14.3711, 10.1515]
        altitude:(list) [70, 0]
    '''
    
    # Met Norway Locationforecast resource
    ## test ds format
    norway=WeatherDataSource(name='Met Norway Locationforecast')
    rep_ds=norway.data(latitude=[67.2828, 68.3737],longitude=[14.3711, 10.1515],altitude=[70, 0],format="ds")
    assert type(rep_ds) is xarray.Dataset
    assert keys_exists(dict(rep_ds.dims),('alt','lat','location','lon','time'))
    
    ### test coords
    assert list(rep_ds.coords)==['alt', 'lat', 'location', 'time', 'lon']
    assert rep_ds.coords['time'].dtype=='<M8[ns]'
    assert rep_ds.coords['time'].attrs=={}
    assert rep_ds.coords['location'].dtype=='<U18'
    assert numpy.all(rep_ds.coords['location'].values==['[67.2828, 14.3711]','[68.3737, 10.1515]'])
    assert rep_ds.coords['location'].attrs=={'name': '[latitude,longitude]'}
    assert rep_ds.coords['lat'].dtype=='float64'
    assert rep_ds.coords['lat'].attrs=={'name': 'latitude', 'unit': 'degrees_north'}
    assert numpy.all(rep_ds.coords['lat'].values==[67.2828,68.3737])
    assert rep_ds.coords['lon'].dtype=='float64'
    assert rep_ds.coords['lon'].attrs=={'name': 'longitude', 'unit': 'degrees_east'}
    assert numpy.all(rep_ds.coords['lon'].values==[10.1515,14.3711])
    assert rep_ds.coords['alt'].dtype=='float64'
    assert rep_ds.coords['alt'].attrs=={'name': 'altitude', 'unit': 'meters'}
    assert numpy.all(rep_ds.coords['alt'].values==[0.,70])
    
    ### test data variable
    assert list(rep_ds.data_vars) == ['1001', '3001', '2001', '4002']
    assert rep_ds.data_vars['1001'].dtype == 'float64'
    assert rep_ds.data_vars['1001'].attrs == {'id': 1001, 'name': 'Instantaneous temperature at 2m', 'description': None, 'unit': 'Celcius'}    
    assert rep_ds.data_vars['3001'].dtype == 'float64'
    assert rep_ds.data_vars['3001'].attrs == {'id': 3001, 'name': 'Instantaneous RH at 2m (%)', 'description': None, 'unit': '%'}    
    assert rep_ds.data_vars['2001'].dtype == 'float64'
    assert rep_ds.data_vars['2001'].attrs == {'id': 2001, 'name': 'Precipitation', 'description': None, 'unit': 'mm'}
    assert rep_ds.data_vars['4002'].dtype == 'float64'
    assert rep_ds.data_vars['4002'].attrs == {'id': 4002, 'name': 'Instantaneous wind speed at 2m', 'description': None, 'unit': 'm/s'}

    ### test ds attribute
    assert type(rep_ds.attrs) is dict
    assert keys_exists(rep_ds.attrs,('weatherRessource','longitude','latitude','timeStart','timeEnd','parameters'))
    assert rep_ds.attrs['weatherRessource']=='Met Norway Locationforecast'
    assert rep_ds.attrs['longitude']==[10.1515,14.3711]
    assert rep_ds.attrs['latitude']==[67.2828,68.3737]
    assert rep_ds.attrs['parameters']==['1001', '3001', '2001', '4002']

    ###test conversion dataframe
    assert rep_ds.to_dataframe().shape[1]==4
    assert rep_ds.to_dataframe().index.names==['alt', 'lat', 'location', 'lon', 'time']

    # format= json
    rep_json=norway.data(latitude=[67.2828, 68.3737],longitude=[14.3711, 10.1515],altitude=[70,0.],format="json")

    assert type(rep_json) is list
    for el in range(len(rep_json)):
        assert(type(rep_json[el]) is  dict)
        assert keys_exists(rep_json[0],('timeStart', 'timeEnd', 'interval', 'weatherParameters', 'locationWeatherData'))
        assert rep_json[el]['weatherParameters']==[1001, 3001, 2001, 4002]
        assert rep_json[el]['locationWeatherData'][0]['longitude'] in [14.3711, 10.1515]
        assert rep_json[el]['locationWeatherData'][0]['latitude'] in [67.2828, 68.3737]
        assert rep_json[el]['locationWeatherData'][0]['altitude'] in [70,0.]
       

def testDataStationsFMIForecasts():
    '''
    Test 'FMI weather forecasts' data function for two parameters by argument

    Params:
    -------
        latitude:(list) [67.2828, 68.3737]
        longitude: (list) [14.3711, 10.1515]
        altitude:(list) [70, 0]
    
    Problem: parameter 1901 is not in get.parameter()
    -------
    '''
    
    ## test ds format
    fmi_forecasts=WeatherDataSource(name='FMI weather forecasts')
    rep_ds=fmi_forecasts.data(latitude=[67.2828, 68.3737],longitude=[14.3711, 10.1515],altitude=[70, 0],format="ds")
    assert type(rep_ds) is xarray.Dataset
    assert keys_exists(dict(rep_ds.dims),('alt','lat','location','lon','time'))

def testDataStationsFMI():
    '''
    Test 'Finnish Meteorological Institute measured data' data function for one parameter by argument

    Params:
    -------
        stationId= [101104,101533]
        parameters = [1002,3002]
        timeStart = '2020-06-12'
        timeEnd = '2020-07-03'
        timeZone = 'UTC'

    '''
    
    ## test ds format
    fmi=WeatherDataSource(name='Finnish Meteorological Institute measured data')
    rep_ds=fmi.data(
        stationId=[101104,101533],
        parameters=[1002,3002],
        timeStart = '2020-06-12',
        timeEnd = '2020-07-03',
        timeZone='UTC',
        format="ds")
    assert type(rep_ds) is xarray.Dataset
    assert keys_exists(dict(rep_ds.dims),('alt','lat','location','lon','time'))

    ### test coords
    assert list(rep_ds.coords)==['lat', 'location', 'time', 'lon', 'alt']
    assert rep_ds.coords['time'].dtype=='<M8[ns]'
    assert rep_ds.coords['time'].attrs=={}
    assert rep_ds.coords['location'].dtype=='int64'
    assert numpy.all(rep_ds.coords['location'].values==[101104, 101533])
    assert rep_ds.coords['lat'].dtype=='float64'
    assert rep_ds.coords['lat'].attrs=={'name': 'latitude', 'unit': 'degrees_north'}
    assert numpy.all(rep_ds.coords['lat'].values==[60.81397, 63.08898])
    assert rep_ds.coords['lon'].dtype=='float64'
    assert rep_ds.coords['lon'].attrs=={'name': 'longitude', 'unit': 'degrees_east'}
    assert numpy.all(rep_ds.coords['lon'].values==[23.49825, 24.26084])
    assert rep_ds.coords['alt'].dtype=='float64'
    assert rep_ds.coords['alt'].attrs=={'name': 'altitude', 'unit': 'meters'}
    assert rep_ds.coords['alt'].values==[0.]
    
    ### test data variable
    assert list(rep_ds.data_vars) == ['1002', '3002']
    assert rep_ds.data_vars['1002'].dtype == 'float64'
    assert rep_ds.data_vars['1002'].attrs == {'id': 1002, 'name': 'Mean air temperature at 2m', 'description': None, 'unit': 'Celcius'}    
    assert rep_ds.data_vars['3002'].dtype == 'float64'
    assert rep_ds.data_vars['3002'].attrs == {'id': 3002, 'name': 'Mean RH at 2m', 'description': None, 'unit': '%'}    

    ### test ds attribute
    assert type(rep_ds.attrs) is dict
    assert keys_exists(rep_ds.attrs,('weatherRessource','longitude','latitude','timeStart','timeEnd','parameters'))
    assert rep_ds.attrs['weatherRessource']=='Finnish Meteorological Institute measured data'
    assert rep_ds.attrs['longitude']==[23.49825, 24.26084]
    assert rep_ds.attrs['latitude']==[60.81397, 63.08898]
    assert rep_ds.attrs['parameters']==['1002', '3002']

    ###test conversion dataframe
    assert rep_ds.to_dataframe().shape[1]==2
    assert rep_ds.to_dataframe().index.names==['alt', 'lat', 'location', 'lon', 'time']

    # format= json
    rep_json=fmi.data(
        stationId=[101104,101533],
        parameters=[1002,3002],
        timeStart = '2020-06-12',
        timeEnd = '2020-07-03',
        timeZone='UTC',
        format="json")
    
    assert type(rep_json) is list
    for el in range(len(rep_json)):
        assert type(rep_json[el]) is dict
        assert keys_exists(rep_json[el],('timeStart', 'timeEnd', 'interval', 'weatherParameters', 'locationWeatherData'))
        assert rep_json[el]['weatherParameters']==[1002, 3002]
        assert rep_json[el]['locationWeatherData'][0]['longitude'] in [23.49825, 24.26084]
        assert rep_json[el]['locationWeatherData'][0]['latitude'] in [60.81397, 63.08898]
        assert rep_json[0]['locationWeatherData'][0]['altitude']==0.0

def testDataStationsLandbruks():
    '''
    Test 'Landbruksmeteorologisk tjeneste' data function for one parameter by argument

    Params:
    -------
        stationId= [46,98]
        parameters = [1002,3002]
        timeStart = '2020-06-12'
        timeEnd = '2020-07-03'
        timeZone = 'UTC'
    
    Problem: responses is empty this endpoint are not available problem with location

    '''
    
    ## test ds format
    land=WeatherDataSource(name='Landbruksmeteorologisk tjeneste')
    rep_ds=land.data(
        stationId=[46,98],
        parameters=[1002,3002],
        timeStart = '2020-06-12',
        timeEnd = '2020-07-03',
        timeZone='UTC',
        format="ds")
    assert type(rep_ds) is xarray.Dataset
    assert keys_exists(dict(rep_ds.dims),('alt','lat','location','lon','time'))

