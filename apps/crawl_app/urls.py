from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^orca$', views.orca),
    url(r'^nytimes$', views.nytimes),
    url(r'^youtube$', views.youtube)
]