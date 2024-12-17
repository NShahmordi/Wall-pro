# basic URL Configurations 
from django.urls import include, path 
# import routers 
from rest_framework import routers 
  
# import everything from views 
from .views import *
  
#set the router
router = routers.DefaultRouter() 


router.register(r'users', UserSerializersViewSet) 
router.register(r'Ads', AdvertismentsSerializersViewSet) 
router.register(r'Category',CategorySerializersViewSet) 
router.register(r'City', CitySerializersViewSet) 
router.register(r'Rooms', RoomSerializersViewSet)
router.register(r'Message', MessageSerializersViewSet) 


  
# specify URL Path for rest_framework 
urlpatterns = [ 
    path('', include(router.urls)), 
    path('api-auth/', include('rest_framework.urls')) 
] 