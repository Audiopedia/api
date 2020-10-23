
import graphene
from graphene_django import DjangoObjectType

from .models import Language, Track, Playlist, Topic

class LanguageType(DjangoObjectType):
    class Meta:
        model = Language
        fields = ("name", "audio_url", "published")

class TrackType(DjangoObjectType):
    class Meta:
        model = Track
        fields = ("title", "index", "audio_url", "transcript", "duration", "created_at", "updated_at", "active", "published")

class PlaylistType(DjangoObjectType):
    class Meta:
        model = Playlist
        fields = ("title", "index", "audio_url", "active", "published", "tracks")

class TopicType(DjangoObjectType):
    class Meta:
        model = Topic
        fields=("title", "index", "audio_url", "active", "published", "playlists")

class LanguageInput(graphene.InputObjectType):
    name = graphene.String()
    audio_url = graphene.String()
    published = graphene.Boolean()

class TrackInput(graphene.InputObjectType):
    index = graphene.ID()
    title = graphene.String()
    audio_url = graphene.String()
    transcript = graphene.String()
    duration = graphene.String()
    created_at = graphene.DateTime()
    updated_at = graphene.DateTime()
    active = graphene.Boolean()
    published = graphene.Boolean()
    
class PlaylistInput(graphene.InputObjectType):
    index = graphene.ID()
    title = graphene.String()
    audio_url = graphene.String()
    active = graphene.Boolean()
    published = graphene.Boolean()
    tracks = graphene.List(TrackInput)

class TopicInput(graphene.InputObjectType):
    index = graphene.ID()
    title = graphene.String()
    audio_url = graphene.String()
    active = graphene.Boolean()
    published = graphene.Boolean()
    playlists = graphene.List(PlaylistInput)

class CreateLanguage(graphene.Mutation):
    class Arguments:
        input = PlaylistInput(required=True) # why is this required??
    
    ok = graphene.Boolean()
    language = graphene.Field(LanguageType)

    @staticmethod
    def mutate(root, info, input=None):
        ok = True
        language_instance = Language(
            name=input.name,
            audio_url = input.audio_url,
            published = input.published,
            )
        topic_instance.save()
        topic_instance.playlists.set(playlists)
        return CreateTopic(ok=ok, topic=topic_instance)
 
class CreateTopic(graphene.Mutation):
    class Arguments:
        input = TopicInput(required=True)
    
    ok = graphene.Boolean()
    topic = graphene.Field(TopicType)

    @staticmethod
    def mutate(root, info, input=None):
        ok = True
        playlists = []
        for playlist_input in input.playlists:
            playlist = Playlist.objects.get(pk=playlist_input.index)
            if playlist is None:
                return CreateTopic(ok=False, playlist=None)
            playlists.append(playlist)
        topic_instance = Topic(
            title=input.title,
            audio_url = input.audio_url,
            active = input.active,
            published = input.published,
            )
        topic_instance.save()
        topic_instance.playlists.set(playlists)
        return CreateTopic(ok=ok, topic=topic_instance)
        
class UpdateTopic(graphene.Mutation):
    class Arguments:
        index = graphene.ID(required=True)
        title = graphene.String(required=True)
        audio_url = graphene.String()

    ok = graphene.Boolean()
    topic = graphene.Field(TopicType)

    @staticmethod
    def mutate(root, info, index, title, audio_url=None):
        ok = False
        topic_instance = Topic.objects.get(pk=index)
        if topic_instance:
            ok = True
            playlists = []
            for playlist_input in input.playlists:
                playlist = Playlist.objects.get(pk=playlist_input.index)
                if playlist is None:
                    return UpdateTopic(ok=False, playlist=None)
                playlists.append(playlist)
            topic_instance.title = title
            topic_instance.audio_url = audio_url
            topic_instance.save()
            topic_instance.playlists.set(playlists)
            return UpdateTopic(ok=ok, topic=topic_instance)
        return UpdateTopic(ok=ok, topic=None)

class DeleteTopic(graphene.Mutation):
    class Arguments:
        index = graphene.ID()
    
    ok = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, **kwargs):
        obj = Topic.objects.get(pk=kwargs["index"])
        obj.delete()
        return cls(ok=True)


class CreatePlaylist(graphene.Mutation):
    class Arguments:
        input = PlaylistInput(required=True)
    
    ok = graphene.Boolean()
    playlist = graphene.Field(PlaylistType)

    @staticmethod
    def mutate(root, info, input=None):
        ok = True
        tracks = []
        for track_input in input.tracks:
            track = Track.objects.get(pk=track_input.index)
            if track is None:
                return CreatePlaylist(ok=False, playlist=None)
            playlists.append(playlist)
        playlist_instance = Playlist(
            title=input.title,
            audio_url = input.audio_url,
            active = input.active,
            published = input.published,
            )
        playlist_instance.save()
        playlist_instance.tracks.set(tracks)
        return CreatePlaylist(ok=ok, playlist=playlist_instance)
        
class UpdatePlaylist(graphene.Mutation):
    class Arguments:
        index = graphene.ID(required=True)
        title = graphene.String(required=True)
        audio_url = graphene.String()

    ok = graphene.Boolean()
    playlist = graphene.Field(PlaylistType)

    @staticmethod
    def mutate(root, info, index, title, audio_url=None):
        ok = False
        playlist_instance = Playlist.objects.get(pk=index)
        if playlist_instance:
            ok = True
            tracks = []
            for track_input in input.tracks:
                track = Track.objects.get(pk=track_input.index)
                if track is None:
                    return UpdatePlaylist(ok=False, track=None)
                tracks.append(track)
            playlist_instance.title = title
            playlist_instance.audio_url = audio_url
            playlist_instance.save()
            playlist_instance.tracks.set(tracks)
            return UpdatePlaylist(ok=ok, track=track_instance)
        return UpdatePlaylist(ok=ok, track=None)

class DeletePlaylist(graphene.Mutation):
    class Arguments:
        index = graphene.ID()
    
    ok = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, **kwargs):
        obj = Playlist.objects.get(pk=kwargs["index"])
        obj.delete()
        return cls(ok=True)

class CreateTrack(graphene.Mutation):
    class Arguments:
        input = TrackInput(required=True)
    
    ok = graphene.Boolean()
    playlist = graphene.Field(TrackType)

    @staticmethod
    def mutate(root, info, input=None):
        ok = True
        track_instance = Track(
            title=input.title,
            audio_url = input.audio_url,
            transcript = input.transcript,
            duration = input.duration,
            created_at = graphene.DateTime(),
            updated_at = graphene.DateTime(),
            active = input.active,
            published = input.published
            )
        track_instance.save()
        return CreateTrack(ok=ok, track=track_instance)

class UpdateTrack(graphene.Mutation):
    class Arguments:
        index = graphene.ID(required=True)
        transcript = graphene.String()
        audio_url = graphene.String()
        duration = graphene.String()

    ok = graphene.Boolean()
    track = graphene.Field(TrackType)

    @staticmethod
    def mutate(root, info, index, duration, transcript=None, audio_url=None):
        ok = False
        track_instance = Track.objects.get(pk=index)
        if track_instance:
            ok = True
            if audio_url:
                track_instance.audio_url = audio_url
            if transcript:
                track_instance.transcript = transcript
            if duration:
                track_instance.duration = duration
            track_instance.save()
            return UpdateTrack(ok=ok)
        return UpdateTrack(ok=ok)

class DeleteTrack(graphene.Mutation):
    class Arguments:
        index = graphene.ID()
    
    ok = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, **kwargs):
        obj = Track.objects.get(pk=kwargs["index"])
        obj.delete()
        return cls(ok=True)

class Mutation(graphene.ObjectType):
    create_topic = CreateTopic.Field()
    update_topic = UpdateTopic.Field()
    delete_topic = DeleteTopic.Field()
    create_playlist = CreatePlaylist.Field()
    update_playlist = UpdatePlaylist.Field()
    delete_playlist = DeletePlaylist.Field()
    create_track = CreateTrack.Field()
    update_track = UpdateTrack.Field()
    delete_track = DeleteTrack.Field()
    create_language = CreateLanguage.Field()

class Query(graphene.ObjectType):
    all_languages = graphene.List(LanguageType)
    all_tracks = graphene.List(TrackType)
    all_playlists = graphene.List(PlaylistType)
    all_topics = graphene.List(TopicType)

    # def resolve_audios(self, info, **kwargs):
    #     return Audio.objects.all()

schema = graphene.Schema(query=Query, mutation=Mutation)