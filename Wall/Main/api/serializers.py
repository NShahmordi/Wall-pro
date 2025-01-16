from rest_framework import serializers
from django.core.exceptions import PermissionDenied
from ..models import Users, Advertisement, City, Category, Message, Room, AdvertisementImage, Bookmark

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
    images = AdvertisementImageSerializer(many=True, read_only=True)
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Advertisement
        fields = [
            'id',
            'title',
            'description',
            'price',
            'created_at',
            'updated_at',
            'slug',
            'owner',
            'city',
            'category',
            'status',
            'images',
        ]

class BookmarkSerializer(serializers.ModelSerializer):
    advertisement = AdvertisementSerializer()

    class Meta:
        model = Bookmark
        fields = [
            'id',
            'advertisement',
            'created_at',
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
    first_image = serializers.SerializerMethodField()

    class Meta:
        model = Advertisement
        fields = [
            'title',
            'short_description',
            'first_image',
        ]

    def get_short_description(self, obj):
        if obj.description:
            return ' '.join(obj.description.split()[:5]) + '...' if len(obj.description.split()) > 5 else obj.description
        return None

    def get_first_image(self, obj):
        first_image = obj.images.first()
        return AdvertisementImageSerializer(first_image).data if first_image else None
