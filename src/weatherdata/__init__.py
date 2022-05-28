# -*- python -*-
#
#       Copyright INRIA - CIRAD - INRA
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
# ==============================================================================


import pkg_resources
from .version import version as _version
__version__ = _version
try:
    version = pkg_resources.require("weatherdata")[0].version
    __version__ = version
except:
    version = __version__

from . import ipm
from .ipm import *









