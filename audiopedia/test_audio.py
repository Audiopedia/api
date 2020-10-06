import pytest
from django.test import TestCase
from graphene.test import Client
 
from audios.models import *
from audios.schema import schema

from collections import OrderedDict 

query_track = """
query {
  allTracks {
    title
    index
    audioUrl
    transcript
    duration
    active
    published
  }
}
"""
create_track = """
mutation createTrack {
  createTrack(input: {
    title: "This is a test question?",
    index: 0,
    audioUrl:"www.test.url",
    transcript: "This is a test transcript.",
    duration: 50,
    active: true,
    published: true
  }) {
    ok
    track {
      index
    }
  }
}
"""

update_track = """
mutation updateTrack {
  updateTrack(index: 1, transcript: "Hello", duration: "0:02:30") {
		ok
    track {
      id
    }
  }
}
"""

"""
mutation updateTrack {
  updateTrack(index: 1, transcript: "Hello", duration: "0:02:30") {
		ok
    track {
      id
    }
  }
}
"""

@pytest.mark.django_db
class TestSchemas(TestCase):
    def setUp(self):
        self.client = Client(schema)
 
    def test_create_track(self):
        result = self.client.execute(create_track)
        print(Track.objects.all())

        assert result["data"] == OrderedDict({
          "createTrack": {
            "ok": True,
            "track": {
              "index": "0"
            }
          }
        })
        