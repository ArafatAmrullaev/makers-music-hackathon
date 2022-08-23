from re import M
from django.db import models

from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.


User = get_user_model()


class Artist(models.Model):
    name = models.CharField(max_length=50)
    profile_pic = models.ImageField(upload_to='artists')


class Genre(models.Model):
    title = models.CharField(max_length=50)



class Song(models.Model):
    title = models.CharField(max_length=50)
    artist = models.ForeignKey(Artist, related_name="songs", on_delete=models.CASCADE)
    cover = models.ImageField(upload_to='songs')
    year = models.DateField(auto_now=True)
    audiofile = models.FileField(upload_to='tracks')
    lyrics = models.TextField()
    genre = models.ManyToManyField(Genre, related_name="songs")


class Album(models.Model):
    title = models.CharField(max_length=50)
    artist = models.ForeignKey(Artist, related_name="albums", on_delete=models.CASCADE)
    song = models.ManyToManyField(Song, related_name="albums")
    cover = models.ImageField(upload_to='albums')
    genre = models.ManyToManyField(Genre, related_name="albums")
    year = models.DateField(auto_now=True)
    desc = models.TextField(blank=True, null=True)
    @property
    def average_rating(self):
        ratings = [rating.value for rating in self.ratings.all()]
        if ratings:
            return sum(ratings)/len(ratings)
        else:
            return 0


class MyPlaylist(models.Model):
    title = models.CharField(max_length=50)
    song = models.ManyToManyField(Song, related_name="myplaylists")
    cover = models.ImageField(upload_to='myplaylists', blank=True, null=True)
    created_at = models.DateField(auto_now=True)
    user = models.ForeignKey(User, related_name='myplaylists', on_delete=models.CASCADE)


class Rating(models.Model):
    user = models.ForeignKey(User, related_name='ratings', on_delete=models.CASCADE)
    album = models.ForeignKey(Album, related_name='ratings', on_delete=models.CASCADE)
    value = models.IntegerField(choices=[(1,1), (2,2), (3,3), (4,4), (5,5)])


class Comment(models.Model):
    user = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    album = models.ForeignKey(Album, related_name='comments', on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Like(models.Model):
    user = models.ForeignKey(User, related_name='likes', on_delete=models.CASCADE)
    album = models.ForeignKey(Album, related_name='likes', on_delete=models.CASCADE)


class Favourite(models.Model):
    user = models.ForeignKey(User, related_name='favourite', on_delete=models.CASCADE)
    song = models.ForeignKey(Song, related_name='favourite', on_delete=models.CASCADE)

