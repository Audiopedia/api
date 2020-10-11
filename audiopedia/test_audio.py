import pytest
from django.test import TestCase
from graphene.test import Client
 
from audios.models import *
from audios.schema import schema

import collections

query_track = """
query {
  allTracks {
    id
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
    title: "How are germs mostly spread?",
    index: 0,
    audioUrl: "www.test.url",
    transcript: "Germs are spread through X,Y, and Z.",
    duration: 33,
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
  updateTrack(id: 1, active: false) {
	ok
    track {
        active
    }
  }
}
"""

delete_track = """
mutation deleteTrack {
  deleteTrack(id: 1) {
	ok
  }
}
"""

create_playlist = """
mutation createPlaylist {
    createPlaylist(input: {
		index: 0,
        title: "Cleanliness",
        audioUrl: "www.test.url",
        active: true,
        published: true,
        tracks: [1]
  }) {
        ok
        playlist {
            id
        }
    }
}
"""

query_playlist = """
query {
    allPlaylists {
        id
        title
        index
        audioUrl
        active
        published
        tracks {
            id
            title
            index
            audioUrl
            transcript
            duration
            active
            published
        }
    }
}
"""

update_playlist = """
mutation updatePlaylist {
  updatePlaylist(id: 1, active: false) {
	ok
    playlist {
        active
    }
  }
}
"""

delete_playlist = """
mutation deletePlaylist {
  deletePlaylist(id: 1) {
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
          'title': 'How are germs mostly spread?',
          'index': 0,
          'id': '1',
          'audioUrl': 'www.test.url',
          'transcript': 'Germs are spread through X,Y, and Z.',
          'duration': 33,
          'active': True,
          'published': True
        }

    def test_update_track(self):
        self.client.execute(create_track)
        result = self.client.execute(update_track)
        assert result["data"] == collections.OrderedDict([('updateTrack', {'ok': True, 'track': {'active': False}})])

    def test_delete_track(self):
        self.client.execute(create_track)
        result = self.client.execute(delete_track)
        assert result["data"] == collections.OrderedDict([('deleteTrack', {'ok': True})])
        # Query tracks to make sure there are no tracks
        result = self.client.execute(query_track)
        assert result == {'data': {'allTracks': []}}
    
    def test_create_playlist(self):
        self.client.execute(create_track)
        result = self.client.execute(create_playlist)
        assert result == {'data': collections.OrderedDict([('createPlaylist', {'ok': True, 'playlist': {'id': '1'}})])}

    def test_query_playlist(self):
        self.client.execute(create_track)
        self.client.execute(create_playlist)
        result = self.client.execute(query_playlist)
        assert result == {'data': {'allPlaylists': [{'id': '1', 'title': 'Cleanliness', 'index': 0, 'audioUrl': 'www.test.url', 'active': True, 'published': True, 'tracks': [{'id': '1', 'title': 'How are germs mostly spread?', 'index': 0, 'audioUrl': 'www.test.url', 'transcript': 'Germs are spread through X,Y, and Z.', 'duration': 33, 'active': True, 'published': True}]}]}}

    def test_update_playlist(self):
        self.client.execute(create_track)
        self.client.execute(create_playlist)
        result = self.client.execute(update_playlist)
        assert result == {'data': collections.OrderedDict([('updatePlaylist', {'ok': True, 'playlist': {'active': False}})])}
    
    def test_delete_playlist(self):
        self.client.execute(create_track)
        self.client.execute(create_playlist)
        result = self.client.execute(delete_playlist)
        assert result == {'data': collections.OrderedDict([('deletePlaylist', {'ok': True})])}
        

        