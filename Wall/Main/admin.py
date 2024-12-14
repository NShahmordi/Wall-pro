from django.contrib import admin

# Register your models here.
from .models import Users,Advertisement

@admin.register(Users)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    
    

@admin.register(Advertisement)
class CustomAdvertisementAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner','category' , 'city')
