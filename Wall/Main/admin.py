from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Users, Advertisement, City, Category, Message, Room
from .forms import *

@admin.register(Users)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'phone_number', 'is_staff', 'slug')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone_number', 'slug')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name', 'phone_number', 'password1', 'password2', 'slug'),
        }),
    )
    ordering = ('username',)
    filter_horizontal = ()
    list_filter = ()
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

@admin.register(Advertisement)
class CustomAdvertisementAdmin(admin.ModelAdmin):
    list_display = ("title", "price", "city", "category", "created_at", "updated_at")
    list_filter = ("city", "category", "created_at")  
    search_fields = ("title", "description") 
    ordering = ("-created_at",)  
    prepopulated_fields = {'slug': ('title',)}

@admin.register(City)
class CustomCityAdmin(admin.ModelAdmin):
    list_display = ('city_name',)
    search_fields = ('city_name',)

@admin.register(Category)
class CustomCategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'parent')
    list_filter = ('parent',)      
    search_fields = ('category_name',)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'room', 'sender', 'content', 'timestamp', 'updated_at')
    list_filter = ('timestamp', 'updated_at')

admin.site.register(Room)