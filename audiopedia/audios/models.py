from django.db import models
from datetime import datetime

class Language(models.Model):
    name = models.CharField(max_length=100)
    audio_url = models.URLField()
    published = models.BooleanField(default=True)

class Track(models.Model):
    title = models.CharField(max_length=200)
    index = models.IntegerField(unique=True)
    audio_url = models.URLField()
    transcript = models.TextField()
    duration = models.IntegerField() # Duration in seconds
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)
    active = models.BooleanField(default=True)
    published = models.BooleanField(default=True)

class Playlist(models.Model):
    title = models.CharField(max_length=200)
    index = models.IntegerField(unique=True)
    audio_url = models.URLField()
    active = models.BooleanField(default=True)
    published = models.BooleanField(default=True)
    tracks = models.ManyToManyField(Track)

class Topic(models.Model):
    title = models.CharField(max_length=200)
    index = models.IntegerField(unique=True)
    audio_url = models.URLField()
    active = models.BooleanField(default=True)
    published = models.BooleanField(default=True)
    playlists = models.ManyToManyField(Playlist)

