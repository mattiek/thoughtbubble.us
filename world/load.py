import os
from django.contrib.gis.utils import LayerMapping
from .models import *


world_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data/TM_WORLD_BORDERS-0.3.shp'))

def run(verbose=True):
    print world_shp
    print WorldBorder.objects.count()
    lm = LayerMapping(WorldBorder, world_shp, worldborder_mapping,
                      transform=False, encoding='iso-8859-1')
    print WorldBorder.objects.count()