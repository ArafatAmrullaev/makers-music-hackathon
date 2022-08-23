from django.contrib import admin

from django.contrib import admin

from .models import Artist, Genre, Song, Album, Comment, Rating, Like, Favourite, MyPlaylist
admin.site.register(Artist)
admin.site.register(Song)
admin.site.register(Album)
admin.site.register(Comment)
admin.site.register(Rating)
admin.site.register(Like)
admin.site.register(Favourite)
admin.site.register(MyPlaylist)
admin.site.register(Genre)