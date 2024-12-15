from django.urls import path, include
from Main.views import chatPage as ChatpageViews
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path("", ChatpageViews, name="chat-page"),

    # login-section
    path("auth/login/", LoginView.as_view
         (template_name="chat/LoginPage.html"), name="login-user"),
    path("auth/logout/", LogoutView.as_view(), name="logout-user"),
]
