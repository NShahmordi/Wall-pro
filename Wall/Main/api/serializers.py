from rest_framework import serializers
from ..models import Users, Advertisement, City, Category, Message, Room,AdvertisementImage
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
            'uploaded_at',
                  ]
from rest_framework.exceptions import PermissionDenied

class AdvertisementSerializer(serializers.ModelSerializer):
    city = CitySerializers() 
    category = CategorySerializers() 
    owner = UserSerializers(read_only=True)
    images = AdvertisementImageSerializer(many=True, required=False)

    class Meta:
        model = Advertisement
        fields = [
            'title',
            'description',
            'price',
            'slug',
            'owner',
            'city',
            'category',
            'shirt_size',
            'images',
        ]

    def update(self, instance, validated_data):
        user = self.context['request'].user 
        if instance.owner != user:  
            raise PermissionDenied("You are not the owner of this advertisement.")

        images_data = validated_data.pop('images', None)
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.price = validated_data.get('price', instance.price)
        instance.slug = validated_data.get('slug', instance.slug)
        instance.city = validated_data.get('city', instance.city)  
        instance.category = validated_data.get('category', instance.category) 

        instance.shirt_size = validated_data.get('shirt_size', instance.shirt_size)
        instance.save()

        if images_data:
            instance.images.all().delete()
            for image_data in images_data:
                AdvertisementImage.objects.create(advertisement=instance, **image_data)

        return instance

class MessageSerializers(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = [
                   'id',  
                   'room', 
                   'sender',
                   'message',
                   ]

    def update(self, instance, validated_data):
        instance.message = validated_data.get('message', instance.message)
        instance.room = validated_data.get('room', instance.room)
        instance.save()
            
class RoomSerializers(serializers.ModelSerializer):
    messages = MessageSerializers(many=True)
    class Meta:
        model = Room
        fields = [ 
                  'token', 
                  'users',
                ]
        
class ListOfAdvertisementSerializer(serializers.ModelSerializer):
    short_description = serializers.SerializerMethodField()
    class Meta:
        model = Advertisement
        fields = [
            'title',
            'short_description',
            'image',
            'price',
            'created_at',
            'city',
            'category',
        ]        
    def get_short_description(self, obj):
        if obj.description:
            return ' '.join(obj.description.split()[:5]) +\
                '...' if len(obj.description.split()) > 5\
                    else obj.description
        return None

