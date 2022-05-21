# openalea.weatherdata

**Authors**:

* [Marc Labadie](https://github.com/mlabadie)
* [Christian Fournier](https://github.com/christian34)
* [Christophe Pradal](https://github.com/pradal)

**Institutes:** INRAE/CIRAD

**Licence:** [GPL-3](https://www.gnu.org/licenses/gpl-3.0.txt)
 
**Status:** Python package

**Citation:**

## Description

WeatherData is a Python package that transforms weather data retrieved from [agroservices](https://github.com/openalea/agroservices) in an efficient Python data structure (xarray) to facilitate its usage in Python and OpenAlea.

## Installation

```shell
conda create -n weatherdata python pandas numpy xarray 
conda activate weatherdata

git clone https://github.com/H2020-IPM-openalea/agroservices.git
cd agroservices
python setup.py install

git clone https://github.com/H2020-IPM-openalea/weatherdata.git
cd weatherdata
python setup.py install
```

## Requierements

* python>=3
* pandas
* numpy
* xarray
* agroservices
* requests (agroservices)
* appdirs (agroservices)
* bs4 (agroservices)
* colorlog (agroservices)
* requests_cache (agroservices)
* xarray (weatherdata)
* pandas
* jupyter

## Documentation

You can see the complete documentation with tutorials at: xxx

## Contributing
All contributions, bug reports, bug fixes, documentation improvements, enhancements, and ideas are welcome.

A detailed overview on how to contribute can be found in the [contributing guide](http://virtualplants.github.io/contribute/devel/workflow-github.html#workflow-github).

### contributors

<a href="https://github.com/H2020-IPM-openalea/weatherdata/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=H2020-IPM-openalea/weatherdata" />
</a>
