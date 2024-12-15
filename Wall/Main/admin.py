from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Users,Advertisement 
from .forms import *
from .models import Room
@admin.register(Users)
class CustomUserAdmin(UserAdmin):
    add_form = SignUpForm
    form = CustomUserChangeForm
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
    list_display = ('title', 'owner','category' , 'city')
    prepopulated_fields = {'slug': ('title', 'category', 'city')}
    search_fields = ('title', 'city', 'category')
    list_filter = ('city', 'category')

