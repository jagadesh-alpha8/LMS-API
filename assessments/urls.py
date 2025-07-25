from django.urls import path
from .views import *

urlpatterns = [
    path('', subscribed_assessments_with_questions),
    # path('submit/', submit_assessment_answers),
]
