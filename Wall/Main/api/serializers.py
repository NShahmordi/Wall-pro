from rest_framework import serializers
from django.core.exceptions import PermissionDenied
from ..models import Users, Advertisement, City, Category, Message, Room, AdvertisementImage

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

class CitySerializers(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['city_name']    

class CategorySerializers(serializers.ModelSerializer):
    parent = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields = [
            'category_name',
            'parent',
        ]
    
    def get_parent(self, obj):
        if obj.parent:
            return CategorySerializers(obj.parent).data
        return None

class AdvertisementImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvertisementImage
        fields = [
            'id',
            'image',
        ]

class AdvertisementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertisement
        fields = [
            'title',
            'description',
            'price',
            'image',
            'created_at',
            'owner',
        ]

class MessageSerializers(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = [
            'id',  
            'room', 
            'sender',
            'content',
            'timestamp',
            'updated_at',
        ]

    def update(self, instance, validated_data):
        instance.message = validated_data.get('message', instance.message)
        instance.room = validated_data.get('room', instance.room)
        instance.save()
            
class RoomSerializers(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = [
            'token',
            'user1',
            'user2',
            'created_at',
            'messages',
        ]

class ListOfAdvertisementSerializer(serializers.ModelSerializer):
    short_description = serializers.SerializerMethodField()
    class Meta:
        model = Advertisement
        fields = [
            'title',
            'short_description',
            'image',
        ]        
    def get_short_description(self, obj):
        if obj.description:
            return ' '.join(obj.description.split()[:5]) +\
                '...' if len(obj.description.split()) > 5\
                    else obj.description
        return None
