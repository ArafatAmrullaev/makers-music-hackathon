from dataclasses import field, fields
from multiprocessing import context
from pyexpat import model
from rest_framework import serializers

from .models import Artist, Favourite, Song, Album, Comment, Rating, Like, MyPlaylist


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = '__all__'
    
    def to_representation(self, instance):
        request = self.context.get('request')
        rep = super().to_representation(instance)
        rep['songs'] = SongSerializer(instance.song.all(), many=True, context={'request': request}).data
        rep['albums'] = AlbumSerializer(instance.album).data

class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = '__all__'
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['added_to_favourite'] = False
        request = self.context.get('request')
        if request.user.is_authenticated:
            rep['added_to_favourite'] = Favourite.objects.filter(user=request.user, song=instance).exists()
        return rep

class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = '__all__'
    def to_representation(self, instance):
        request = self.context.get('request')
        rep = super().to_representation(instance)
        rep['comments'] = CommentSerializer(instance.comments.all(), many=True).data
        rep['likes'] = instance.likes.all().count()
        rep['rating'] = instance.average_rating
        rep['liked_by_user'] = False
        rep['user_rating'] = 0
        
    
        if request.user.is_authenticated:
            rep['liked_by_user'] = Like.objects.filter(user=request.user, album=instance).exists()
            if Rating.objects.filter(user=request.user, album=instance).exists():
                rating = Rating.objects.get(user=request.user, album=instance)
                rep['user_rating'] = rating.value

        return rep

class MyPlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyPlaylist
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        exclude = ['user']

    def create(self, validated_data):
        validated_data['user'] = self.context.get('request').user
        return super().create(validated_data)

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['user'] = instance.user.email
        return rep

class FavouriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favourite
        exclude = ('user', )


