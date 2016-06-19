from django.conf.urls import url

from atlas import views

urlpatterns = [
    url(r'^atlas/lista/$', views.lista, name='lista'),
    url(r'^$', views.cargar, name='index'),
    url(r'^$',  views.cargar, name='cargar'), # NEW MAPPING!
]
