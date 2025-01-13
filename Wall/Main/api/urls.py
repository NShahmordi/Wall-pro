from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import UserSerializersViewSet, AdvertismentsSerializersViewSet, RoomSerializersViewSet, MessageSerializersViewSet

router = DefaultRouter()
router.register(r'users', UserSerializersViewSet)
router.register(r'advertisements', AdvertismentsSerializersViewSet)
router.register(r'rooms', RoomSerializersViewSet)
router.register(r'messages', MessageSerializersViewSet)

urlpatterns = [
    path('', include(router.urls)),
]