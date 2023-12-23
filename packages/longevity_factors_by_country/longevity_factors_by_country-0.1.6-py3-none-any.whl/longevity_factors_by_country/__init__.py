# read version from installed package
from importlib.metadata import version
import longevity_factors_by_country
import clean_data
from database import *

__version__ = version("longevity_factors_by_country")