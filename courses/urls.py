from django.urls import path
from . import views

urlpatterns = [
    path('', views.my_subscribed_courses_with_videos, name='my-courses'),
]