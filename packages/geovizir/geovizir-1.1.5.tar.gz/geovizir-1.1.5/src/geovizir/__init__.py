# read version from installed package
from importlib.metadata import version
__version__ = version("geovizir")

from geovizir.features import *
from geovizir.scales import *
