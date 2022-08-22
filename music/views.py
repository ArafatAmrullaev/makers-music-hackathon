from urllib import request
from django.shortcuts import render

from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from .serializers import ArtistSerializer, SongSerializer, AlbumSerializer, FavouriteSerializer, CommentSerializer, MyPlaylistSerializer
from .models import Artist, MyPlaylist, Song, Album, Rating, Comment, Like, Favourite
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from .permissions import IsAdminOrReadOnly, IsAuthor, IsAuthorOrReadOnly
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import filters, mixins

class ArtistViewSet(ModelViewSet, GenericViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['name']


    @swagger_auto_schema(manual_parameters=[openapi.Parameter('name', openapi.IN_QUERY, 'search artist by name', type=openapi.TYPE_STRING)])
    @action(methods=["GET"], detail=False)
    def search(self, request,):
        name = request.query_params.get("name")
        queryset = self.get_queryset()

        if name:
            queryset = queryset.filter(name__icontains=name)

        serializer = ArtistSerializer(queryset, many=True, context={'request':request})
        return Response(serializer.data, 200)


class SongViewSet(ModelViewSet, GenericViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['title', 'artist']


    @swagger_auto_schema(manual_parameters=[openapi.Parameter('title', openapi.IN_QUERY, 'search song by title', type=openapi.TYPE_STRING)])
    @action(methods=["GET"], detail=False)
    def search(self, request,):
        title = request.query_params.get("title")
        queryset = self.get_queryset()

        if title:
            queryset = queryset.filter(title__icontains=title)

        serializer = SongSerializer(queryset, many=True, context={'request':request})
        return Response(serializer.data, 200)


class AlbumViewSet(ModelViewSet, GenericViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['title', 'genre', 'artist']


    @swagger_auto_schema(manual_parameters=[openapi.Parameter('title', openapi.IN_QUERY, 'search album by title', type=openapi.TYPE_STRING)])
    @action(methods=["GET"], detail=False)
    def search(self, request,):
        title = request.query_params.get("title")
        queryset = self.get_queryset()

        if title:
            queryset = queryset.filter(title__icontains=title)

        serializer = AlbumSerializer(queryset, many=True, context={'request':request})
        return Response(serializer.data, 200)

class CommentViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.UpdateModelMixin, GenericViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsAuthor]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

@api_view(['GET'])
def toggle_like(request, a_id):
    user = request.user
    album = get_object_or_404(Album, id=a_id)

    if Like.objects.filter(user=user, album=album).exists():
        Like.objects.filter(user=user, album=album).delete()
    else:
        Like.objects.create(user=user, album=album)

    return Response('Like toggled', 200)

@api_view(['POST'])
def add_rating(request, a_id):
    user = request.user
    album = get_object_or_404(Album, id=a_id)
    value = request.POST.get('value')

    if not user.is_authenticated:
        raise ValueError('authentication credentials are not provided')

    if not value:
        raise ValueError('value is required')
    
    if Rating.objects.filter(user=user, album=album).exists():
        rating = Rating.objects.get(user=user, album=album)
        rating.value = value
        rating.save()

    else:
        Rating.objects.create(user=user, album=album, value=value)

    return Response('rating created', 201)



@api_view(['GET'])
def add_to_favourite(request, s_id):
    user = request.user
    song = get_object_or_404(Song, id=s_id)

    if Favourite.objects.filter(user=user, song=song).exists():
        Favourite.objects.filter(user=user, song=song).delete()
    else:
        Favourite.objects.create(user=user, song=song)

    return Response('Added to Favourite', 200)

class FavouriteViewSet(mixins.ListModelMixin, GenericViewSet):
    queryset = Favourite.objects.all()
    serializer_class = FavouriteSerializer

    def filter_queryset(self, queryset):
        new_queryset = queryset.filter(user=self.request.user)
        return new_queryset


class MyPlaylistViewSet(ModelViewSet, GenericViewSet):
    queryset = MyPlaylist.objects.all()
    serializer_class = MyPlaylistSerializer
    permission_classes = [IsAuthenticated, IsAuthor]
    # if object.is_public == False:
    #     def filter_queryset(self, queryset):
    #         new_queryset = queryset.filter(user=self.request.user.username)
    #         return new_queryset
# def get_serializer_context(self):
#     context = super().get_serializer_context()
#     context['user'] = self.request.user
#     return context