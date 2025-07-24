from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Assessment, UserAssessmentSubmission
from .serializers import AssessmentSerializer, UserAssessmentSubmissionSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def eligible_assessments(request):
    user = request.user
    assessments = Assessment.objects.all()
    eligible = []
    for a in assessments:
        total = a.course.video_set.count()
        watched = a.course.video_set.filter(userwatchedvideo__user=user).count()
        if total > 0 and total == watched:
            eligible.append(a)
    serializer = AssessmentSerializer(eligible, many=True, context={'request': request})
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_assessment(request):
    serializer = UserAssessmentSubmissionSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        submission = serializer.save()
        return Response({
            "message": "Assessment submitted successfully.",
            "score": submission.score,
            "attempt": submission.attempt_number
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
