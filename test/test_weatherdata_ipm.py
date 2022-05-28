import pandas
import xarray
import numpy
from weatherdata.ipm import WeatherDataHub, WeatherDataSource

wdh= WeatherDataHub()
list_resources = list(wdh.list_resources.name)

def keys_exists(dict_, keys, test = all):
    return test(key in dict_ for key in keys)

def testListRessource():
    '''
    Test list_ressource function
    '''
    rep= wdh.list_resources
    assert type(rep) is pandas.DataFrame, rep
    assert list(rep.columns) == ['name', 'description', 'parameters']
    assert list(rep.name)== ['Met Norway Locationforecast',
                             'Met Éireann Locationforecast',
                             'DMI Pointweather service',
                             'SLU Lantmet service',
                             'Deutsche Wetterdienst location forecast by IPM Decisions',
                             'Deutsche Wetterdienst EU Area location forecast by IPM Decisions',
                             'Euroweather seasonal gridded weather data and forecasts  by IPM Decisions',
                             'MeteoFrance location forecast by IPM Decisions',
                             'FMI weather forecasts',
                             'Finnish Meteorological Institute measured data',
                             'Landbruksmeteorologisk tjeneste',
                             'MeteoBot API',
                             'Fruitweb',
                             'Metos',
                             'Meteodata by Météo Concept']
    assert rep.shape == (15,3)

def testGetRessource():
    '''
    Test get resource functoin for all ressources
    '''

    for name in list_resources:
        rep=wdh.get_ressource(name=name)
        if isinstance(rep,WeatherDataSource):
            pass
""" Problem with json load 
def testStationId():
    '''
    Test station_id function for all ressources
    '''
    wds_station_ids={name:wdh.get_ressource(name=name).stations for name in list_resources}

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
"""

def testParameters():
    '''
    Test parameters function for all resources
    '''
    wds_parameters={name:wdh.get_ressource(name=name).parameter for name in list_resources}

    # Met Norway Locationforecast resource
    assert type(wds_parameters['Met Norway Locationforecast']) is pandas.DataFrame
    assert list(wds_parameters['Met Norway Locationforecast'].id) == [1001, 2001, 3001, 4002]

    # FMI weather forecasts resource
    assert type(wds_parameters['FMI weather forecasts']) is pandas.DataFrame
    assert list(wds_parameters['FMI weather forecasts'].id) == [1001, 1901, 2001, 3001, 4002, 5001]

    # Finnish Meteorological Institute measured data resource
    assert type(wds_parameters['Finnish Meteorological Institute measured data']) is pandas.DataFrame
    assert list(wds_parameters['Finnish Meteorological Institute measured data'].id) == [1002, 2001, 3002, 4003]

    # Landbruksmeteorologisk tjeneste resource
    assert type(wds_parameters['Landbruksmeteorologisk tjeneste']) is pandas.DataFrame
    assert list(wds_parameters['Landbruksmeteorologisk tjeneste'].id) == [1002, 1003, 1004, 2001, 3002, 4003]

    # MeteoBot API resource
    assert type(wds_parameters['MeteoBot API']) is pandas.DataFrame
    assert list(wds_parameters['MeteoBot API'].id) == [1001, 2001, 3001, 4002]
    
    # Fruitweb resource
    assert type(wds_parameters['Fruitweb']) is pandas.DataFrame
    assert list(wds_parameters['Fruitweb'].id) == [1001, 2001, 3001, 4002] 

    # Metos resource
    assert type(wds_parameters['Metos']) is pandas.DataFrame
    assert list(wds_parameters['Metos'].id) == [1001, 2001, 3001, 4002] 

def testEndpoint():
    '''
    Test endpoint function for all ressources
    '''
    wds_endpoints={name:wdh.get_ressource(name=name).endpoint for name in list_resources}

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
    wds_check_forcast={name:wdh.get_ressource(name=name).forecast for name in list_resources}

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
