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
"""

class Audio(models.Model):
    question = models.TextField(blank=True)
    language = models.TextField(blank=True)
    category = models.TextField(blank=True)