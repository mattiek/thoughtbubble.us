import os
from django.contrib.gis.utils import LayerMapping
from neighborhood.models import *


nhood_shape = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data/ZillowNeighborhoods-OH.shp'))

def run(verbose=True):
    print nhood_shape
    print Neighborhood.objects.count()
    lm = LayerMapping(Neighborhood, nhood_shape, neighborhood_mapping)
    print Neighborhood.objects.count()