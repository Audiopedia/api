from django.db import models

# We want a new model...
# We need a model that matches audiopedia:
# So we would want a "audio" app, not links
# Each audiofile model will contain
"""
* id
* question
* language
* category
* actual audio file path??

from audios.models import Audio
Audio.objects.create(question="How can cleanliness prevent sickness?", language="en", category="Cleanliness")
Audio.objects.create(question="What drugs should I avoid to stay healthy?", language="en", category="Substance Abuse")
Audio.objects.create(question="Which helper foods should I eat regularly?", language="en", category="Nutrition")

class Audio(models.Model):
    question = models.TextField(blank=True)
    language = models.TextField(blank=True)
    category = models.TextField(blank=True)
"""


class Language(models.Model):
    name = models.CharField(max_length=100)
    audio_url = models.URLField()
    published = models.BooleanField(default=True)

class Topic(models.Model):
    title = models.CharField(max_length=200)
    index = models.IntegerField(unique=True)
    audio_url = models.URLField()
    active = model.BooleanField(default=True)
    published = models.BooleanField(default=True)
    playlists = models.ManyToManyField(Playlist)

class Playlist(models.Model):
    title = models.CharField(max_length=200)
    index = models.IntegerField(unique=True)
    audio_url = models.URLField()
    active = model.BooleanField(default=True)
    published = models.BooleanField(default=True)
    tracks = models.ManyToManyField(Track)

class Track(models.Model):
    title = models.CharField(max_length=200)
    index = models.IntegerField(unique=True)
    audio_url = models.URLField()
    transcript = models.TextField()
    duration = models.DurationField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    active = model.BooleanField(default=True)
    published = models.BooleanField(default=True)

