import pandas
import xarray
import numpy
from weatherdata.ipm import WeatherDataHub, WeatherDataSource

wdh= WeatherDataHub()
list_resources = list(wdh.list_resources.name)

def keys_exists(dict_, keys, test = all):
    return test(key in dict_ for key in keys)

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

