from rest_framework import serializers
from ..models import Users, Advertisement, City, Category, Message, Room 

class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = [
                'id',
                'first_name', 
                'last_name', 
                'email', 
                'username',
                'phone_number',
                'slug',
            ]
class AdvertisementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertisement
        fields = [
            'title',
            'description',
            'image',
            'price',
            'slug',
            'owner',
            'city',
            'category',
            'shirt_size',
        ]

class CitySerilizers(serializers.ModelSerializer):
    class Meta:
        models = City
        fields = [
            'city_name'
        ]    
        
class CategorySerilizers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'category_name'
        ]        
class RoomSerilizers(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = [
            'token',
            'users',
        ]        
class MessageSerilizers(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = [
            'room',
            'sender',
            'message',
        ]        