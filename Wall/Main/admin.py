from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Users, Advertisement, City, Category
from .forms import *
from .models import Room

@admin.register(Users)
class CustomUserAdmin(UserAdmin):
    add_form = SignUpForm
    form = CustomUserChangeForm
    prepopulated_fields = {'slug': ('id',)}
    list_display = ("username","email", "is_staff", "is_active",)
    list_filter = ("username","email", "is_staff", "is_active",)
    fieldsets = (
        (None, {"fields": ("username","first_name","last_name","phone_number","email", "password","slug")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "username","first_name","last_name","phone_number",
                "email", "password1" ,"password2", "is_staff",
                "is_active", "groups", "user_permissions","slug"
            )}
        ),
    )
    search_fields = ("username",)
    ordering = ("username",)
    
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
    list_display = ('category_name',)
    search_fields = ('category_name',)
    

    