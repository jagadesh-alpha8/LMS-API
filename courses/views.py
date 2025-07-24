from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Course, Subscription
from .serializers import CourseSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_subscribed_courses_with_videos(request):
    subscriptions = Subscription.objects.filter(user=request.user).select_related('course')
    courses_data = []
    for subscription in subscriptions:
        print(subscription.course.name)  # Debug log
        course = subscription.course
        course_data = CourseSerializer(course).data
        courses_data.append(course_data)
    
    return Response(courses_data)