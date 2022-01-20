# Note test of function and ressources

## Met Norway Locationforecast

**comment:** No major problem identified

* station_ids: 'no stations for this ressources'
* endpoint: '/weatheradapter/yr/'
* forecast: True
* data return a xarray.dataset
  * parameters: ['1001', '3001', '2001', '4002']

## FMI weather forecasts

**comments:** Problem with meta-information 
The description of the weatherparameter 1901 is not present in the description of weatherparameters (get_parameter)

* station_ids: 'no stations for this ressources'
* endpoint: '/weatheradapter/fmi/forecasts'
* forecast: True
* data() function is blocked due to not description of 1901 parameters

## Finnish Meteorological Institute measured data

**comments:** only 204 stations works/208   
station not working: 137188, 855522,137189,126737(Internal Server Error).    
On the 204 station which responses compilation of all data return an error of data dimension "conflicting sizes for dimension 'time': length 505 on 'time' and length 421 on '1002'" (this problem provide from station 101649 i don't know why but timestart change timeStart": "2020-06-15T12:00:00Z)

* station_ids: return a list of 208 weatherStationIds
* endpoint: '/weatheradapter/fmi/'
* forecast: False
* data() function is blocked due to not description of 1901 parameters

## Landbruksmeteorologisk tjeneste

**comments**: Present in weatherdatasource files but not present in IPM Plateform
Is this resource still available?

* station_ids: return a list of 92 weatherStationIds
* endpoint: '/ipmdecisions/getdata/'
* forcast: False
* data: Problem with location coords, not responses of ipm plateform xarray.dataset is empty

## 'MeteoBot API'

**Comments**: Problem of connection with credentials see (test_agroservices)

* station_ids: 508 WeatherStationId available
* endpoint:'/weatheradapter/meteobot/'
* forecast: False
* data: Problem avec location not responses xarray.dataset is empty

## 'Fruitweb'

**Comments**: Problem of connection with credentials see (test_agroservices)

* station_ids: 'no stations for this ressources'
* endpoint:'/weatheradapter/davisfruitweb/'
* forecast: False
* data: Problem avec location not responses xarray.dataset is empty

## 'Metos'

**Comments**: Problem of connection with credentials see (test_agroservices)

* station_ids: 'no stations for this ressources'
* endpoint:'/weatheradapter/metos/'
* forecast: False
* data: Problem avec location not responses xarray.dataset is empty
