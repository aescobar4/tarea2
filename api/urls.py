"""api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from ti import views

urlpatterns = [
    path('', views.index),
    path('artists', views.artists),
    path('artists/<str:artist_id>', views.artistsId),
    path('artists/<str:artist_id>/albums', views.albumsPerArtist),
    path('albums/<str:album_id>', views.albumsId),
    path('albums', views.albums),
    path('albums/<str:album_id>/tracks', views.tracksPerAlbum),
    path('tracks/<str:track_id>', views.tracksId),
    path('tracks', views.tracks),
    path('artists/<str:artist_id>/tracks', views.artistTracks),
    path('artists/<str:artist_id>/albums/play', views.playArtist),
    path('albums/str:album_id>/tracks/play', views.playAlbum),
]