#from models import UploadFile
import datetime
import taggit
from django import forms


from geonode.maps.models import Map
from geonode.people.models import Profile
from django.utils.translation import ugettext_lazy as _

from geonode.base.models import Region

from geonode.maps.models import Map
from geonode.maps.forms import MapForm
from django import forms
from django.forms.extras.widgets import SelectDateWidget
from atlas.models import Atlas, Hoja_atlas, Autor, Tabla, Leyenda, Imagen, Grafica



class AtlasForm(forms.ModelForm):
    class Meta:
        model = Atlas
        #fields = '__all__'



#class Hoja_atlasForm(MapForm):
class Hoja_atlasForm(forms.ModelForm):
    class Meta:
      model = Hoja_atlas
      #exclude = ['zoom']
      fields =['atlas','tema','nombre','texto','color','thumbnail','descripcion','mapa','autor','informacion_bibliografica']
      #Para la version sin mapa 
      #fields =['atlas','tema','nombre','texto','color','thumbnail','descripcion','mapa','mapaEstatico','autor','informacion_bibliografica']
      #Para agregar lo del zoom usamos exclude
      #Mecesito que en las formas solo aparezcan los campos de hoja
      #No sobrrescribir los campos
      #Se debe cambiar el comportamiento para que mis campos extiendan de un mapa ya he
      #fields = '__all__'

class AutorForm(forms.ModelForm):

    class Meta:
      model = Autor
      #fields = ['nombre','apellido_paterno','apellido_materno']


class AutorForm(forms.ModelForm):

    class Meta:
      model = Autor
      #fields = '__all__'


class TablaForm(forms.ModelForm):

    class Meta:
      model = Tabla
      #fields = '__all__'


class LeyendaForm(forms.ModelForm):

    class Meta:
      model = Leyenda


class ImagenForm(forms.ModelForm):

    class Meta:
      model = Imagen


class GraficaForm(forms.ModelForm):

    class Meta:
      model = Grafica
