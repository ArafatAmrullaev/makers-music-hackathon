from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import ArtistViewSet, CommentViewSet, GenreViewSet, SongViewSet, AlbumViewSet, toggle_like, add_rating, add_to_favourite, FavouriteViewSet, MyPlaylistViewSet

router = DefaultRouter()
router.register('artists', ArtistViewSet)
router2 = DefaultRouter()
router2.register('songs', SongViewSet)
router3 = DefaultRouter()
router3.register('albums', AlbumViewSet)
router4 = DefaultRouter()
router4.register('favourites', FavouriteViewSet)
router.register('comments', CommentViewSet)
router.register('myplaylists', MyPlaylistViewSet)
router.register('genre', GenreViewSet)

from .views import Home # new

urlpatterns = [
    path('', include(router.urls)),
    path('', include(router2.urls)),
    path('', include(router3.urls)),
    path('albums/toggle_like/<int:a_id>/', toggle_like),
    path('albums/add_rating/<int:a_id>/', add_rating),
    path('songs/add_to_favourite/<int:s_id>/', add_to_favourite),
    path('', include(router4.urls)),
    path("", Home.as_view(), name="home"),
]