from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import UserSerializersViewSet, AdvertisementViewSet, RoomSerializersViewSet, MessageSerializersViewSet, BookmarkViewSet

router = DefaultRouter()
router.register(r'users', UserSerializersViewSet)
router.register(r'advertisements', AdvertisementViewSet)
router.register(r'rooms', RoomSerializersViewSet)
router.register(r'messages', MessageSerializersViewSet)
router.register(r'bookmarks', BookmarkViewSet, basename='bookmark')

urlpatterns = [
    path('', include(router.urls)),
]