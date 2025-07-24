from django.urls import path
from .views import can_attempt_assessment, AssessmentListView, SubmitAssessmentView

urlpatterns = [
    path('can-attempt/<int:course_id>/', can_attempt_assessment),
    path('list/', AssessmentListView.as_view()),
    path('submit/', SubmitAssessmentView.as_view()),
]
