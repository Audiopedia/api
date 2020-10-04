import pytest
from django.test import TestCase
from graphene.test import Client
 
from audios.models import *
from audios.schema import schema

list_tracks_query = """
    query {
        allTracks {
            id
        }
    }
"""

create_blog_mutation = """
     mutation CreateBlog($input: BlogInputType!) {
        createBlog(input: $input) {
            blog {
                id
                title
                author {
                    id
                    name
                }
            }
            ok
        }
    }
"""

@pytest.mark.django_db
class TestSchemas(TestCase):

    def setUp(self):
        self.client = Client(schema)
 
    def test_single_query(self):
        result = self.client.execute(list_tracks_query)
        self.assertDictEqual({"reporter": {"id": "1"}}, result["data"])