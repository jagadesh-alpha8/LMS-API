from django.urls import path
from .views import *

urlpatterns = [
    path('', subscribed_assessments_with_questions, name='list_assessments'),
    path('submit/', submit_assessment, name='submit_assessment'),
]
