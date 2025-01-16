from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserSerializersViewSet, AdvertismentsSerializersViewSet, RoomSerializersViewSet, MessageSerializersViewSet, AdvertisementViewSet, BookmarkViewSet, RoomCreateAPIView

router = DefaultRouter()
router.register(r'users', UserSerializersViewSet)
router.register(r'advertisements', AdvertismentsSerializersViewSet)
router.register(r'rooms', RoomSerializersViewSet)
router.register(r'messages', MessageSerializersViewSet)
router.register(r'advertisement', AdvertisementViewSet)
router.register(r'bookmarks', BookmarkViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('create-room/', RoomCreateAPIView.as_view(), name='create-room'),
]