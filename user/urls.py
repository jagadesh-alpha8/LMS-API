from django.urls import path
from .views import LoginAPIView
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('login/', LoginAPIView.as_view()),
]
