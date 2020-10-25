import graphene
from graphene_django import DjangoObjectType
from datetime import timedelta
from django.utils import timezone

from .models import Language, Track, Playlist, Topic

class LanguageType(DjangoObjectType):
    class Meta:
        model = Language
        fields = ("id", "name", "audio_url", "published")

class TrackType(DjangoObjectType):
    class Meta:
        model = Track
        fields = ("id", "title", "index", "audio_url", "transcript", "duration", "created_at", "updated_at", "active", "published")

class PlaylistType(DjangoObjectType):

    # get tracks by playlist workaround?
    # tracks = graphene.List(TrackType)

    # @graphene.resolve_only_args
    # def resolve_tracks(self):
    #     return self.tracks.all()

    class Meta:
        model = Playlist
        fields = ("id", "title", "index", "audio_url", "active", "published", "tracks")

class TopicType(DjangoObjectType):
    class Meta:
        model = Topic
        fields=("id", "title", "index", "audio_url", "active", "published", "playlists")

class LanguageInput(graphene.InputObjectType):
    name = graphene.String(description="Name of the language")
    audio_url = graphene.String(description="URL to audio directory associated with the language")
    published = graphene.Boolean(description="Visible to user if true")

class TrackInput(graphene.InputObjectType):
    index = graphene.ID(description="Position of the track within a playlist")
    title = graphene.String(description="Title of the track")
    audio_url = graphene.String(description="URL to the audio file associated with this track")
    transcript = graphene.String(description="Transcript that goes along with this track")
    duration = graphene.Int(description="Duration of the track in seconds")
    active = graphene.Boolean(description="Inactivate to temporarily delete track and reactivate to recover")
    published = graphene.Boolean(description="Visible to user if true")
    
class PlaylistInput(graphene.InputObjectType):
    index = graphene.ID(description="Position of the playlist within a topic")
    title = graphene.String(description="Title of the playlist")
    audio_url = graphene.String(description="URL to the audio directory associated with this playlist")
    active = graphene.Boolean(description="Inactivate to temporarily delete playlist and reactivate to recover")
    published = graphene.Boolean(description="Visible to user if true")
    tracks = graphene.List(graphene.ID, description="List of all the IDs of tracks this playlist contains")

class TopicInput(graphene.InputObjectType):
    index = graphene.ID(description="Position/placement of the topic among a list of topics")
    title = graphene.String(description="Title of the topic")
    audio_url = graphene.String(description="URL to the audio directory associated with this topic")
    active = graphene.Boolean(description="Inactivate to temporarily delete topic and reactivate to recover")
    published = graphene.Boolean(description="Visible to user if true")
    playlists = graphene.List(graphene.ID, description="List of all the IDs of playlists this topic contains")

class CreateLanguage(graphene.Mutation):
    class Arguments:
        input = LanguageInput(required=True, description="Look at LanguageInput definition for more details")
    
    ok = graphene.Boolean()
    language = graphene.Field(LanguageType)

    @staticmethod
    def mutate(root, info, input=None):
        ok = True
        lang_instance = Language(
            name = input.name,
            audio_url = input.audio_url,
            published = input.published
            )
        lang_instance.save()
        return CreateLanguage(ok=ok, language=lang_instance)

class UpdateLanguage(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True, description="ID of the language to be updated")
        name = graphene.String(description="New name for the language")
        audio_url = graphene.String(description="New URL")
        published = graphene.Boolean(description="Update published status")

    ok = graphene.Boolean()
    language = graphene.Field(LanguageType)

    @staticmethod
    def mutate(root, info, id, name=None, published=None, audio_url=None):
        ok = False
        lang_instance = Language.objects.get(pk=id)
        if lang_instance:
            ok = True
            if audio_url:
                lang_instance.audio_url = audio_url
            if name:
                lang_instance.transcript = name
            if published != None:
                lang_instance.published = published

            lang_instance.save()
            return UpdateLanguage(ok=ok, language=lang_instance)
        return UpdateLanguage(ok=ok, language=None)

class DeleteLanguage(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True, description="ID of the language to be deleted")
    
    ok = graphene.Boolean()

    @staticmethod
    def mutate(root, info, id):
        obj = Language.objects.get(pk=id)
        obj.delete()
        return DeleteLanguage(ok=True)

class CreateTopic(graphene.Mutation):
    class Arguments:
        input = TopicInput(required=True, description="Look at TopicInput definition for more details")
    
    ok = graphene.Boolean()
    topic = graphene.Field(TopicType)

    @staticmethod
    def mutate(root, info, input=None):
        ok = True
        playlists = []
        for playlist_id in input.playlists:
            playlist = Playlist.objects.get(pk=playlist_id)
            if playlist is None:
                return CreateTopic(ok=False, playlist=None)
            playlists.append(playlist)
        topic_instance = Topic(
            index = input.index,
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
        id = graphene.ID(required=True, description="ID of the topic to be updated")
        index = graphene.Int(description="New position of the topic among a list of topics")
        title = graphene.String(description="New title for the topic")
        audio_url = graphene.String(description="New URL")
        active = graphene.Boolean(description="Updated active status")
        published = graphene.Boolean(description="Updated published status")
        playlists = graphene.List(graphene.ID, description="New playlist order")

    ok = graphene.Boolean()
    topic = graphene.Field(TopicType)

    @staticmethod
    def mutate(root, info, id, index=None, active=None, published=None, playlists=[], title=None, audio_url=None):
        ok = False
        topic_instance = Topic.objects.get(pk=id)
        if topic_instance:
            ok = True
            new_playlists = []
            for playlist_id in playlists:
                playlist = Playlist.objects.get(pk=playlist_id)
                if playlist is None:
                    return UpdateTopic(ok=False, playlist=None)
                playlists.append(new_playlists)

            if index: topic_instance.index = index
            if title: topic_instance.title = title
            if audio_url: topic_instance.audio_url = audio_url
            if active != None: topic_instance.active = active
            if published != None: topic_instance.published = published

            topic_instance.save()
            topic_instance.playlists.set(new_playlists)
            return UpdateTopic(ok=ok, topic=topic_instance)
        return UpdateTopic(ok=ok, topic=None)

class DeleteTopic(graphene.Mutation):
    class Arguments:
        id = graphene.ID(description="ID of the topic to be deleted")
    ok = graphene.Boolean()

    @staticmethod
    def mutate(root, info, id):
        obj = Topic.objects.get(pk=id)
        obj.delete()
        return DeleteTopic(ok=True)


class CreatePlaylist(graphene.Mutation):
    class Arguments:
        input = PlaylistInput(required=True, description="Look at PlaylistInput definition for more details")
    
    ok = graphene.Boolean()
    playlist = graphene.Field(PlaylistType)

    @staticmethod
    def mutate(root, info, input=None):
        ok = True
        tracks = []
        for track_id in input.tracks:
            track = Track.objects.get(pk=track_id)
            if track is None:
                return CreatePlaylist(ok=False, playlist=None)
            tracks.append(track)
        playlist_instance = Playlist(
            index = input.index,
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
        id = graphene.ID(required=True, description="ID of the playlist to be updated")
        index = graphene.Int(description="New position of the playlist within a topic")
        title = graphene.String(description="New title")
        audio_url = graphene.String(description="New URL")
        tracks = graphene.List(graphene.ID, description="New ordering of tracks")
        active = graphene.Boolean(description="New active status")
        published = graphene.Boolean(description="New upblished status")

    ok = graphene.Boolean()
    playlist = graphene.Field(PlaylistType)

    @staticmethod
    def mutate(root, info, id, index=None, active=None, published=None, tracks=[], title=None, audio_url=None):
        ok = False
        playlist_instance = Playlist.objects.get(pk=id)
        if playlist_instance:
            ok = True
            new_tracks = []
            for track_id in tracks:
                track = Track.objects.get(pk=track_id)
                if track is None:
                    return UpdatePlaylist(ok=False, track=None)
                new_tracks.append(track)

            if index: playlist_instance.index = index
            if title: playlist_instance.title = title
            if audio_url: playlist_instance.audio_url = audio_url
            if active != None: playlist_instance.active = active
            if published != None: playlist_instance.published = published
            playlist_instance.save()

            if len(tracks): playlist_instance.tracks.set(new_tracks)
            return UpdatePlaylist(ok=ok, playlist=playlist_instance)
        return UpdatePlaylist(ok=ok, playlist=None)

class DeletePlaylist(graphene.Mutation):
    class Arguments:
        id = graphene.ID(description="ID of playlist to be deleted")
    
    ok = graphene.Boolean()

    @staticmethod
    def mutate(root, info, id):
        obj = Playlist.objects.get(pk=id)
        obj.delete()
        return DeletePlaylist(ok=True)

class CreateTrack(graphene.Mutation):
    class Arguments:
        input = TrackInput(required=True, description="Look at TrackInput definition for more details")
    
    ok = graphene.Boolean()
    track = graphene.Field(TrackType)

    @staticmethod
    def mutate(root, info, input=None):
        ok = True
        track_instance = Track(
            index =input.index,
            title=input.title,
            audio_url = input.audio_url,
            transcript = input.transcript,
            duration = input.duration,
            created_at = timezone.now(),
            updated_at = timezone.now(),
            active = input.active,
            published = input.published
            )
        track_instance.save()
        return CreateTrack(ok=ok, track=track_instance)

class UpdateTrack(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True, description="ID of track to be updated")
        index = graphene.Int(description="New position of the track within a playlist")
        transcript = graphene.String(description="New transcript")
        audio_url = graphene.String(description="New URL")
        duration = graphene.String(description="New duration")
        active = graphene.Boolean(description="New active status")
        published = graphene.Boolean(description="New published status")

    ok = graphene.Boolean()
    track = graphene.Field(TrackType)

    @staticmethod
    def mutate(root, info, id, index=None, active=None, published=None, duration=None, transcript=None, audio_url=None):
        ok = False
        track_instance = Track.objects.get(pk=id)
        if track_instance:
            ok = True
            if index:
                track_instance.index = index
            if audio_url:
                track_instance.audio_url = audio_url
            if transcript:
                track_instance.transcript = transcript
            if duration:
                track_instance.duration = duration
            if active != None:
                track_instance.active = active
            if published != None:
                track_instance.published = published

            # Update the updated_at time
            track_instance.updated_at = timezone.now()

            track_instance.save()
            return UpdateTrack(ok=ok, track=track_instance)
        return UpdateTrack(ok=ok, track=None)

class DeleteTrack(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True, description="ID of the track to be deleted")
    
    ok = graphene.Boolean()

    @staticmethod
    def mutate(root, info, id):
        obj = Track.objects.get(pk=id)
        obj.delete()
        return DeleteTrack(ok=True)

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
    update_language = UpdateLanguage.Field()
    delete_language = DeleteLanguage.Field()

class Query(graphene.ObjectType):
    topic = graphene.Field(TopicType, id=graphene.Int())
    playlist = graphene.Field(PlaylistType, id=graphene.Int())

    tracks = graphene.List(TrackType, playlist=graphene.ID())
    playlists = graphene.List(PlaylistType, topic=graphene.ID())

    all_languages = graphene.List(LanguageType)
    all_topics = graphene.List(TopicType)
    all_playlists = graphene.List(PlaylistType)
    all_tracks = graphene.List(TrackType)

    # get topic by id
    def resolve_topic(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Topic.objects.get(pk=id)
        
        return None

    # get playlist by id
    def resolve_playlist(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Playlist.objects.get(pk=id)

        return None

    # get tracks by playlist
    def resolve_tracks(self, info, playlist = None, **kwargs):

        if playlist is not None:            
            return Track.objects.filter(playlist__id=playlist)
        return None

    # get playlist by topic
    def resolve_playlists(self, info, topic = None, **kwargs):

        if topic is not None:            
            return Playlist.objects.filter(topic__id=topic)
        
        return None
    
    # get all languages/topics/playlists/tracks in database
    def resolve_all_languages(self, info, **kwargs):
        return Language.objects.all()

    def resolve_all_topics(self, info, **kwargs):
        return Topic.objects.all()

    def resolve_all_playlists(self, info, **kwargs):
        return Playlist.objects.all()

    def resolve_all_tracks(self, info, **kwargs):
        return Track.objects.all()

schema = graphene.Schema(query=Query, mutation=Mutation)