from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics
from .models import Assessment, UserWatchedVideo, UserAssessmentSubmission
from courses.models import Course, Video
from .serializers import AssessmentSerializer, UserAssessmentSubmissionSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def can_attempt_assessment(request, course_id):
    user = request.user
    course = Course.objects.get(id=course_id)
    total_videos = Video.objects.filter(course=course).count()
    watched = UserWatchedVideo.objects.filter(user=user, video__course=course).count()

    if watched >= total_videos and total_videos > 0:
        return Response({"status": "unlocked", "watched": watched, "total": total_videos})
    else:
        return Response({"status": "locked", "watched": watched, "total": total_videos})


class AssessmentListView(generics.ListAPIView):
    queryset = Assessment.objects.all()
    serializer_class = AssessmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        course_id = self.request.query_params.get('course_id')
        return Assessment.objects.filter(course__id=course_id)


class SubmitAssessmentView(generics.CreateAPIView):
    serializer_class = UserAssessmentSubmissionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
