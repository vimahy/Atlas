import os

import subprocess
import md5
import StringIO
from django.core.files.base import ContentFile
from PIL import Image
import logging
import sys , os, glob
from PIL import Image
import math
import logging

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed, HttpResponseServerError
from django.shortcuts import render_to_response, get_object_or_404
from django.conf import settings
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.utils import simplejson as json
from django.db.models import F


from geonode.maps.views import *
from geonode.documents.models import get_related_documents
from geonode.people.forms import ProfileForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.template import RequestContext, loader
from atlas.models import Atlas, Hoja_atlas, Leyenda, Imagen, Tabla, Grafica, Hoja_atlas, Autor
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.shortcuts import render_to_response
from atlas.forms import AtlasForm,Hoja_atlasForm, AutorForm, TablaForm, LeyendaForm, ImagenForm, GraficaForm, Map 
# Create your views here.

THUMBS_DIR  = '/var/www/geonode/uploaded/Thumbnail/'

def index(request):
    atlas = Atlas.objects.all()
    hojas = Hoja_atlas.objects.all()
    results = Map.objects.all()
    paginator = Paginator(hojas, 11)

    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)

    #Aqui usamos un comado del shell para usar Cutycapt
    for h in hojas:
       if h.thumbnail !='/static/geonode/img/missing_thumb.png':
            identificador = h.nombre
            path = THUMBS_DIR + identificador + '.png'
       #if h.thumbnail=='null'o None:
            print (identificador)
            ident = h.id
            subprocess.check_call(["cutycapt","--url=http://localhost:8000/atlas/"+ str(ident),"--out=" + path,"--delay= 4"])
            path = THUMBS_DIR + identificador + '.png'
            subprocess.call(['mogrify','-resize','300x250',path])
            with open(path) as f:
              data = f.read()
              h.thumbnail.save(identificador+'.png', ContentFile(data))
    #autores = Autor.objects.all()
    #select  detail_url from base_resourcebase, atlas_hoja_atlas where base_resourcebase.id =atlas_hoja_atlas.mapa_id
    #select  * from  atlas_hoja_atlas,atlas_autor where atlas_autor.hoja_id =atlas_hoja_atlas.id
    # {% for a in hojas %}
    #  <li>{{ a.mapa.thumbnail_url }}</li>
    #{% endfor %}
    #
    return render_to_response('atlas/index.html',
        RequestContext(request,{'hojas': hojas,'results': results,'atlas': atlas,"contacts": contacts}))



def hoja(request, hoja_atlas_id):
    try:
        p = Hoja_atlas.objects.get(pk=hoja_atlas_id)
        mapas = p.mapa.all
        imagenes = p.imagen_set.all
        leyendas = p.leyenda_set.all
        graficas = p.grafica_set.all
        tablas = p.tabla_set.all
        #autores = p.autor_set.all
    except Hoja_atlas.DoesNotExist:
        raise Http404
    return render_to_response('atlas/hoja.html', RequestContext(request, {'hoja_atlas': p,'imagenes': imagenes,'leyendas': leyendas,'graficas': graficas,'tablas': tablas,'mapas': mapas,}))


@login_required
def cargarAtlas(request):
    # Get the context from the request.
    context = RequestContext(request)
    
    # A HTTP POST?
    if request.method == 'POST':
        formAtlas = AtlasForm(request.POST)
        # Have we been provided with a valid form?
        if formAtlas.is_valid():
            # Save the new category to the database.
            formAtlas.save(commit=True)
            # Now call the index() view.
            # The user will be shown the homepage.
            return HttpResponseRedirect('/atlas/cargarHoja')
        else:
            # The supplied form contained errors - just print them to the terminal.
            print formAtlas.errors
    else:
        # If the request was not a POST, display the form to enter details.
        formAtlas = AtlasForm()
    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render_to_response('atlas/cargarAtlas.html', {'formAtlas' : AtlasForm }, context)



@login_required
def cargarAutor(request):
    # Get the context from the request.
    context = RequestContext(request)

    # A HTTP POST?
    if request.method == 'POST':
        formAutor = AutorForm(request.POST)
        # Have we been provided with a valid form?
        if formAutor.is_valid():
            # Save the new category to the database.
            formAutor.save(commit=True)
            # Now call the index() view.
            # The user will be shown the homepage.
            return HttpResponseRedirect('/atlas/cargarHoja')
        else:
            # The supplied form contained errors - just print them to the terminal.
            print formAutor.errors
    else:
        # If the request was not a POST, display the form to enter details.
        formAutor = AutorForm()
    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render_to_response('atlas/autor.html', {'formAutor' : AutorForm,}, context)



@login_required
def cargarHoja(request):
    # Get the context from the request.
    context = RequestContext(request)

    # A HTTP POST?
    if request.method == 'POST':
        formHoja_atlas = Hoja_atlasForm(request.POST)
        # Have we been provided with a valid form?
        if formHoja_atlas.is_valid():
            # Save the new category to the database.
            formHoja_atlas.save(commit=True)
            # Now call the index() view.
            # The user will be shown the homepage.
            return HttpResponseRedirect('/atlas/cargarHoja')
        else:
            # The supplied form contained errors - just print them to the terminal.
            print formHoja_atlas.errors
    else:
        # If the request was not a POST, display the form to enter details.
        formHoja_atlas = AtlasForm()
    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render_to_response('atlas/cargarHoja.html', {'formHoja_atlas' : Hoja_atlasForm,}, context)



@login_required
def cargarLeyenda(request):
    if request.method == 'POST':
        formLeyenda = LeyendaForm(request.POST, request.FILES)
        if formLeyenda.is_valid():
            instance = Leyenda(docfile=request.FILES['docfile'])
            instance.save()
            formLeyenda.save()
            return HttpResponseRedirect('/atlas/cargarHoja')
        else:
            print formImagen.errors
    else:
        formImagen = ImagenForm()
    return render(request, 'atlas/cargarLeyenda.html', {'formLeyenda': LeyendaForm})




@login_required
def cargarImagen(request):
    if request.method == 'POST':
        formImagen = ImagenForm(request.POST, request.FILES)
        if formImagen.is_valid():
            instance = Imagen(docfile=request.FILES['docfile'])
            instance.save()
            print ".....imagen.......",instance.docfile
            formImagen.save()
            return HttpResponseRedirect('/atlas/cargarHoja')
        else:
            print formImagen.errors
    else:
        formImagen = ImagenForm()
    return render(request, 'atlas/cargarImagen.html', {'formImagen': ImagenForm})



@login_required
def cargarGrafica(request):
    if request.method == 'POST':
        formGrafica = GraficaForm(request.POST, request.FILES)
        if formGrafica.is_valid():
            instance = Grafica(docfile=request.FILES['docfile'])
            instance.save()
            formGrafica.save()
            return HttpResponseRedirect('/atlas/cargarHoja')
        else:
            print formGrafica.errors
    else:
        formGrafica = GraficaForm()
    return render(request, 'atlas/cargarGrafica.html', {'formGrafica': GraficaForm})


@login_required
def cargarTabla(request):
    if request.method == 'POST':
        formTabla = TablaForm(request.POST, request.FILES)
        if formTabla.is_valid():
            instance = Tabla(docfile=request.FILES['docfile'])
            instance.save()
            formTabla.save()
            return HttpResponseRedirect('/atlas/cargarHoja')
        else:
            print formTabla.errors
    else:
        formTabla = TablaForm()
    return render(request, 'atlas/cargarTabla.html', {'formTabla': TablaForm})
