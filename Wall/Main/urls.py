from django.urls import path
from .views import HomePage, product_detail, user_signup, user_login, user_logout, chatPage, create_ad

urlpatterns = [
    path('', HomePage, name='home'),
    path('product/<slug:slug>/', product_detail, name='product_detail'),
    path('chat/<str:username>/', chatPage, name='chat_page'),
    path('signup/', user_signup, name='signup'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('create-ad/', create_ad, name='create_ad'),
]
