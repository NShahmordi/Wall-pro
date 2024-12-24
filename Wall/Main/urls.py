from django.urls import path
from .views import HomePage, product_detail, user_signup, user_login, user_logout, create_advertisement, edit_ad, chat_history, create_or_get_room, room_detail

urlpatterns = [
    path('', HomePage, name='home'),
    path('product/<slug:slug>/', product_detail, name='product_detail'),
    path('signup/', user_signup, name='signup'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('create-ad/', create_advertisement, name='create_advertisement'),
    path('edit-ad/<slug:slug>/', edit_ad, name='edit_ad'),
    path('chat-history/', chat_history, name='chat_history'),
    path('room/create/<int:user_id>/', create_or_get_room, name='create_room'),
    path('room/<int:room_id>/', room_detail, name='room_detail'),
]
