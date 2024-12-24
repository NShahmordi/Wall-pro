from rest_framework import viewsets

from .serializers import *
from ..models import *

class UserSerializersViewSet(viewsets.ModelViewSet):
    #Define QuerySets
    queryset = Users.objects.all()
    #Specify Serializer
    serializer_class = UserSerializers

class AdvertismentsSerializersViewSet(viewsets.ModelViewSet):
    #Define QuerySets
    queryset = Advertisement.objects.all()
    #Specify Serializer
    serializer_class = AdvertisementSerializer


class CitySerializersViewSet(viewsets.ModelViewSet):
    #Define QuerySets
    queryset = City.objects.all()
    #Specify Serializer
    serializer_class = CitySerializers


class CategorySerializersViewSet(viewsets.ModelViewSet):
    #Define QuerySets
    queryset = Category.objects.all()
    #Specify Serializer
    serializer_class = CategorySerializers


class RoomSerializersViewSet(viewsets.ModelViewSet):
    #Define QuerySets
    queryset = Room.objects.all()
    #Specify Serializer
    serializer_class = RoomSerializers


class MessageSerializersViewSet(viewsets.ModelViewSet):
    #Define QuerySets
    queryset = Message.objects.all()
    #Specify Serializer
    serializer_class = MessageSerializers

