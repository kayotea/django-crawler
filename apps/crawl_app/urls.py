from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.youtube),
    url(r'^orca$', views.orca),
    url(r'^nytimes$', views.nytimes),
    #url(r'^youtube$', views.youtube),
    url(r'^tea$', views.tea)
]