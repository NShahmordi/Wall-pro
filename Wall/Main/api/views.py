from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from ..models import *
from .permissions import IsSuperUserOrOwner, IsAdminOrOwner

class UserSerializersViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UserSerializers
    permission_classes = [IsAuthenticated, IsSuperUserOrOwner]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Users.objects.all()
        return Users.objects.filter(id=user.id)

class AdvertismentsSerializersViewSet(viewsets.ModelViewSet):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    permission_classes = [IsAuthenticated, IsSuperUserOrOwner]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()

class RoomSerializersViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializers
    permission_classes = [IsAuthenticated, IsSuperUserOrOwner]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Room.objects.all()
        return Room.objects.filter(user1=user) | Room.objects.filter(user2=user)

class MessageSerializersViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializers
    permission_classes = [IsAuthenticated, IsSuperUserOrOwner]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Message.objects.all()
        return Message.objects.filter(sender=user)

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

class AdvertisementViewSet(viewsets.ModelViewSet):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    permission_classes = [IsAuthenticated, IsAdminOrOwner]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class BookmarkViewSet(viewsets.ModelViewSet):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer
    permission_classes = [IsAuthenticated, IsAdminOrOwner]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Bookmark.objects.all()
        return Bookmark.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        advertisement = Advertisement.objects.get(id=request.data['advertisement'])
        bookmark, created = Bookmark.objects.get_or_create(user=request.user, advertisement=advertisement)
        if not created:
            bookmark.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        serializer = self.get_serializer(bookmark)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
