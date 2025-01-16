from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserSerializersViewSet,AdvertismentsSerializersViewSet, RoomSerializersViewSet, MessageSerializersViewSet,ListOfAdvertisementViewSet, BookmarkViewSet, RoomCreateAPIView

router = DefaultRouter()
router.register(r'users', UserSerializersViewSet)
router.register(r'ads', AdvertismentsSerializersViewSet,basename='advertisments')
router.register(r'rooms', RoomSerializersViewSet)
router.register(r'messages', MessageSerializersViewSet)
router.register(r'listAds', ListOfAdvertisementViewSet, basename='list of ads')
router.register(r'bookmarks', BookmarkViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('create-room/', RoomCreateAPIView.as_view(), name='create-room'),
]