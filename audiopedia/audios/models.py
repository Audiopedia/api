from django.db import models

class Language(models.Model):
    name = models.CharField(max_length=100)
    audio_url = models.URLField()
    published = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Track(models.Model):
    title = models.CharField(max_length=200)
    index = models.IntegerField(unique=True)
    audio_url = models.URLField()
    transcript = models.TextField()
    duration = models.DurationField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    active = models.BooleanField(default=True)
    published = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class Playlist(models.Model):
    title = models.CharField(max_length=200)
    index = models.IntegerField(unique=True)
    audio_url = models.URLField()
    active = models.BooleanField(default=True)
    published = models.BooleanField(default=True)
    tracks = models.ManyToManyField(Track)

    def __str__(self):
        return self.title

class Topic(models.Model):
    title = models.CharField(max_length=200)
    index = models.IntegerField(unique=True)
    audio_url = models.URLField()
    active = models.BooleanField(default=True)
    published = models.BooleanField(default=True)
    playlists = models.ManyToManyField(Playlist)

    def __str__(self):
        return self.title

