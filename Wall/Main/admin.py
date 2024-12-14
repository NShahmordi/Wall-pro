from django.contrib import admin
from .models import Users,Advertisement 

# Register your models here.
@admin.register(Users)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    prepopulated_fields = {'slug': ('username',)}
@admin.register(Advertisement)
class CustomAdvertisementAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner','category' , 'city')
    prepopulated_fields = {'slug': ('title', 'category', 'city')}
    search_fields = ('title', 'city', 'category')
    list_filter = ('city', 'category')

