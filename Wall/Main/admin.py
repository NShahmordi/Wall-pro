from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Users, Advertisement,AdvertisementImage, City, Category
from .forms import *
from .models import Room

@admin.register(Users)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'phone_number', 'is_staff') 
    fieldsets = (
    (None, {'fields': ('username', 'password')}),
    ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone_number')}),
    ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = ( # add fields to the add user page
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name', 'phone_number', 'password', 'password2'),
        }),
    )
    ordering = ('username',)
    filter_horizontal = ()
    list_filter = ()
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
 
class AdvertisementImageInline(admin.TabularInline):
    model = AdvertisementImage
    extra = 1     
@admin.register(Advertisement)
class CustomAdvertisementAdmin(admin.ModelAdmin):
    list_display = ("title", "price", "city", "category", "created_at", "updated_at")
    list_filter = ("city", "category", "created_at")  
    search_fields = ("title", "description") 
    ordering = ("-created_at",)  
    prepopulated_fields = {'slug': ('title',)}
    inlines = [AdvertisementImageInline]



@admin.register(City)
class CustomCityAdmin(admin.ModelAdmin):
    list_display = ('city_name',)
    search_fields = ('city_name',)
    
@admin.register(Category)
class CustomCategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'parent')
    list_filter = ('parent',)      
    search_fields = ('category_name',)       
    