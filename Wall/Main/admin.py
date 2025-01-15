from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
from .forms import *

# Custom User Admin
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

# Advertisement Image Inline
class AdvertisementImageInline(admin.TabularInline):
    model = AdvertisementImage
    extra = 1

# Custom Advertisement Admin
@admin.register(Advertisement)
class CustomAdvertisementAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'status', 'owner', 'created_at')
    list_filter = ('status', 'created_at', 'updated_at')
    search_fields = ('title', 'description', 'owner__username')
    ordering = ('-created_at',)
    prepopulated_fields = {'slug': ('title',)}
    inlines = [AdvertisementImageInline]

# Custom City Admin
@admin.register(City)
class CustomCityAdmin(admin.ModelAdmin):
    list_display = ('city_name',)
    search_fields = ('city_name',)

# Custom Category Admin
@admin.register(Category)
class CustomCategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'parent')
    list_filter = ('parent',)
    search_fields = ('category_name',)

# Custom Message Admin
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'room', 'sender', 'content', 'timestamp', 'updated_at')
    list_filter = ('timestamp', 'updated_at')

# Custom Bookmark Admin
@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('user', 'advertisement', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'advertisement__title')

# Register Room Model
admin.site.register(Room)