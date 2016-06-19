import datetime
from django.utils import timezone
from haystack import indexes
from geonode.maps.models import Map
from atlas.models import Hoja_atlas


class AtlasIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    nombre = indexes.CharField(model_attr="nombre")
    texto = indexes.CharField(model_attr='texto')
    tema = indexes.CharField(model_attr='tema')
    descripcion = indexes.CharField(model_attr='descripcion')

    def get_model(self):
        return Hoja_atlas



