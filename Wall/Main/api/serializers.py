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
                  'children',
                  ]
        
    def get_children(self, obj):
        if obj.children.exists():
            return CategorySerializers(obj.children.all(), many=True).data
        return None
    
    def get_parent(self, obj):
        if obj.parent:
            return CategorySerializers(obj.parent).data
        return None

class AdvertisementSerializer(serializers.ModelSerializer):
    city = CitySerializers(read_only=True)
    category = CategorySerializers(read_only=True)
    owner = UserSerializers(read_only=True)
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
    
class MessageSerializers(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['room', 'sender', 'message']
class RoomSerializers(serializers.ModelSerializer):
    messages = MessageSerializers(many=True, read_only=True)
    class Meta:
        model = Room
        fields = ['token', 'users']