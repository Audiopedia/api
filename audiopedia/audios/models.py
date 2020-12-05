from django.db import models
from datetime import datetime

class Language(models.Model):
    name = models.CharField(max_length=100, help_text="Name of the language.")
    audio_url = models.URLField(help_text="URL of audios.")
    published = models.BooleanField(default=True, help_text="Decide whether this language is ready for users to see.")

class Track(models.Model):
    title = models.CharField(max_length=200, help_text="Title of the track.")
    index = models.IntegerField(help_text="The position of the track within a playlist.")
    audio_url = models.URLField(help_text="URL to the audio file that goes with this track.")
    transcript = models.TextField(help_text="A string/text transcript that goes along with the audio.")
    duration = models.IntegerField(help_text="Duration in seconds.") # Duration in seconds
    created_at = models.DateTimeField(help_text="When the track was created.", default=datetime.now, blank=True)
    updated_at = models.DateTimeField(help_text="When the track was last updated.", default=datetime.now, blank=True)
    active = models.BooleanField(help_text="Inactivate to temporarily delete track and reactivate to recover.", default=True)
    published = models.BooleanField(help_text="Decide whether this track is ready for users to see.", default=True)
    language = models.ForeignKey("Language", on_delete=models.CASCADE, help_text="The language of the track.")

class Playlist(models.Model):
    title = models.CharField(help_text="The title of the playlist.", max_length=200)
    index = models.IntegerField(help_text="The position of the playlist within a topic.")
    audio_url = models.URLField(help_text="URL to the audio directory associated with the playlist.")
    active = models.BooleanField(help_text="Inactivate to temporarily delete playlist and reactivate to recover.", default=True)
    published = models.BooleanField(help_text="Decide to show or hide the playlist from the users.", default=True)
    tracks = models.ManyToManyField(Track, help_text="A list of all the tracks this playlist contains.")
    language = models.ForeignKey("Language", on_delete=models.CASCADE, help_text="The language of the track.")

class Topic(models.Model):
    title = models.CharField(help_text="The name of the topic.", max_length=200)
    index = models.IntegerField(help_text="The order/position of the topic within the interface.")
    audio_url = models.URLField(help_text="URL to the audio directory associated with the topic.")
    active = models.BooleanField(help_text="Inactivate to temporarily delete topic and reactivate to recover.", default=True)
    published = models.BooleanField(help_text="Decide to show or hide the topic from the users.", default=True)
    playlists = models.ManyToManyField(Playlist, help_text="A list of all the playlists this topic contains.")
    language = models.ForeignKey("Language", on_delete=models.CASCADE, help_text="The language of the track.")

