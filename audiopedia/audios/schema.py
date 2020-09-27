
import graphene
from graphene_django import DjangoObjectType

from .models import Audio

class AudioType(DjangoObjectType):
    class Meta:
        model = Audio

class Query(graphene.ObjectType):
    audios = graphene.List(AudioType)

    def resolve_audios(self, info, **kwargs):
        return Audio.objects.all()