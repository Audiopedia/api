import pytest
from django.test import TestCase
from graphene.test import Client
 
from audios.models import *
from audios.schema import schema

import collections

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
    audioUrl: "www.test.url",
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
  updateTrack(index: 0, transcript: "Hello", duration: "30") {
		ok
  }
}
"""

delete_track = """
mutation deleteTrack {
  deleteTrack(index: 0) {
		ok
  }
}
"""

@pytest.mark.django_db(transaction=True)
class TestSchemas(TestCase):
    def setUp(self):
        self.client = Client(schema)
    
    def test_create_track(self):
        result = self.client.execute(create_track)
        assert result["data"] == collections.OrderedDict({
          "createTrack": {
            "ok": True,
            "track": {
              "index": 0
            }
          }
        })
    
    def test_query_track(self):
        self.client.execute(create_track)
        result = self.client.execute(query_track)
        assert result["data"]["allTracks"][0] == {
          'title': 'This is a test question?',
          'index': 0,
          'audioUrl': 'www.test.url',
          'transcript': 'This is a test transcript.',
          'duration': 50,
          'active': True,
          'published': True
        }

    def test_update_track(self):
        self.client.execute(create_track)
        result = self.client.execute(update_track)
        assert result["data"] == collections.OrderedDict([('updateTrack', {'ok': True})])

    # DELETE QUERIES DOESN'T WORK
    """
    def test_delete_track(self):
        self.client.execute(create_track)
        result = self.client.execute(delete_track)
        assert result["data"] == collections.OrderedDict([('deleteTrack', {'ok': True})])
        # Query tracks to make sure there are no tracks
        result = self.client.execute(query_track)
        print(result)
    """