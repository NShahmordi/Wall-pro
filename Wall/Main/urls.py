from .views import *
from django.urls import path, include
from .views import suggest_ads_template

urlpatterns = [
    path('', HomePage, name='home'),
    path('product/<slug:slug>/', product_detail, name='product_detail'),
    path('signup/', user_signup, name='signup'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('create-ad/', create_advertisement, name='create_advertisement'),
    path('edit-ad/<slug:slug>/', edit_ad, name='edit_ad'),
    path('edit-ad/<slug:slug>/delete/', delete_advertisement, name='delete_advertisement'),
    path('chat-history/', chat_history, name='chat_history'),
    path('room/create/<str:ad_slug>/', create_or_get_room, name='create_room'),
    path('room/<str:token>/', room_detail, name='room_detail'),
    path('delete_image/<int:image_id>/', delete_image, name='delete_image'),
    path('api/', include('Main.api.urls')),
    path('suggestions/', suggest_ads_template, name='advertisement_suggestions'),
]
