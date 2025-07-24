from django.urls import path
from . import views

urlpatterns = [
    # path('', views.all_courses, name='all-courses'),
    path('', views.my_subscribed_courses_with_videos, name='my-courses'),
    # path('courses/<int:course_id>/videos/', views.course_videos, name='course-videos'),
]