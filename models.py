from django.db import models
from geonode.maps.models import Map
from PIL import Image
# Create your models here.

class Atlas(models.Model):
    titulo = models.CharField(max_length=50)
    fecha_de_publicacion = models.DateTimeField(auto_now_add=True)
    num_edicion = models.IntegerField(default=0)
    lugar_de_publicacion = models.CharField(max_length=50)
    editorial = models.CharField(max_length=30)
    numero_paginas = models.IntegerField(default=0)
    descripcion = models.TextField()
    
    def __str__(self):
        return self.titulo

class Autor(models.Model):
    nombre = models.CharField(max_length=50)
    apellido_paterno = models.CharField(max_length=50)
    apellido_materno = models.CharField(max_length=50)
    def __str__(self):
        return self.nombre


#class Hoja_atlas(Map):
class Hoja_atlas(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    autor = models.ManyToManyField(Autor,null=True)
    mapa = models.ManyToManyField(Map,null=True)
    atlas = models.ForeignKey(Atlas)
    #mapa = models.ForeignKey(Map)
    #mapa = models.OneToOneField(Map, primary_key=True)
    tema = models.CharField(max_length=10)
    nombre = models.CharField(max_length=200)
    texto = models.TextField()
    #El color para los distintos temas en hexadecimal
    #leyendas = models.FileField(upload_to='Leyendas/',null=True)
    color = models.CharField(default='#49A8C5',max_length=7)
    thumbnail = models.FileField(default='/static/geonode/img/missing_thumb.png',upload_to='Thumbnail/',
                                null=True,
                                blank=True,
                                verbose_name='Thumbnail')
    #Hacer este campo opcional
    descripcion = models.CharField(max_length=50)
    #La informacion bibliografica pasa a esta tabla
    informacion_bibliografica = models.TextField()
    def __unicode__(self):
        return self.nombre




class Tabla(models.Model):
    titulo = models.CharField(max_length=50)
    descripcion = models.TextField()
    hoja = models.ForeignKey(Hoja_atlas,null=True)
    docfile = models.FileField(upload_to='Tabla',
                                null=True,
                                blank=True,
                                verbose_name=('File'))


class Leyenda(models.Model):
    titulo = models.TextField(max_length=50)
    descripcion = models.TextField()
    hoja = models.OneToOneField(Hoja_atlas,null=True)
    docfile = models.FileField(upload_to='Leyendas/',null=True)


class Imagen(models.Model):
    titulo = models.CharField(max_length=50)
    descripcion = models.TextField()
    hoja = models.ForeignKey(Hoja_atlas,null=True)
    docfile = models.FileField(upload_to='atlas',
                                null=True,
                                blank=True,
                                verbose_name=('File'))




class Grafica(models.Model):
    titulo = models.CharField(max_length=50)
    descripcion = models.TextField()
    hoja = models.ForeignKey(Hoja_atlas,null=True)
    docfile = models.FileField(upload_to='Grafica',
                                null=True,
                                blank=True,
                                verbose_name=('File'))

class MapaEstatico(models.Model):
    titulo = models.CharField(max_length=50)
    descripcion = models.TextField()
    hoja = models.ForeignKey(Hoja_atlas,null=True)
    docfile = models.FileField(upload_to='Mapas',
                                null=True,
                                blank=True,
                                verbose_name=('File'))
