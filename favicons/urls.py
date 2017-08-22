"""URLs for Favicons."""
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.FavFinder.as_view(), name='fav_finder'),
]
