from django.db import models
from base64 import b64encode

class Artist(models.Model):
    id = models.CharField(max_length=22, primary_key=True)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    
class Album(models.Model):
    id = models.CharField(max_length=22, primary_key=True)
    artist_id = models.CharField(max_length=22)
    name = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)

class Track(models.Model):
    id = models.CharField(max_length=22, primary_key=True)
    album_id = models.CharField(max_length=22)
    name = models.CharField(max_length=100)
    duration = models.FloatField()
    times_played = models.IntegerField(default=0)