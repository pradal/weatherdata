"""
Units module of weather data derived from pint library to manage units
"""

import numpy as np
import pint
import pint.unit
import weatherdata


# define registry see pint
units = pint.UnitRegistry()
Quantity= units.Quantity

units.define('wattPar = 1*watt*meter * meter = W_m²')
units.define('PPFD = wattPar / 4.6 / 0.48 = ppfd')
units.define('@alias celsius = Celcius')


del pint