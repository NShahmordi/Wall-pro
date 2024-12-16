from rest_framework import serializers
from .models import Users, Advertisement, City, Category

class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['id',
                  'first_name', 
                  'last_name', 
                  'email', 
                  'username',
                  'phone_number']
        
