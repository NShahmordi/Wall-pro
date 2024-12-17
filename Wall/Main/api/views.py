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
    serializer_class = CitySerilizers


class CategorySerializersViewSet(viewsets.ModelViewSet):
    #Define QuerySets
    queryset = Category.objects.all()
    #Specify Serializer
    serializer_class = CategorySerilizers


class RoomSerializersViewSet(viewsets.ModelViewSet):
    #Define QuerySets
    queryset = Room.objects.all()
    #Specify Serializer
    serializer_class = RoomSerilizers


class MessageSerializersViewSet(viewsets.ModelViewSet):
    #Define QuerySets
    queryset = Message.objects.all()
    #Specify Serializer
    serializer_class = MessageSerilizers

