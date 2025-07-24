from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Course, Subscription, Video
from .serializers import CourseSerializer, VideoSerializer


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def all_courses(request):
#     courses = Course.objects.all()
#     serializer = CourseSerializer(courses, many=True)
#     return Response(serializer.data)


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def my_subscribed_courses(request):
#     subscriptions = Subscription.objects.filter(user=request.user)
#     courses = [subscription.course for subscription in subscriptions]
#     serializer = CourseSerializer(courses, many=True)
#     return Response(serializer.data)


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def course_videos(request, course_id):
#     try:
#         # Check if user is subscribed
#         Subscription.objects.get(user=request.user, course_id=course_id)
#     except Subscription.DoesNotExist:
#         return Response({'detail': 'Not subscribed to this course.'}, status=status.HTTP_403_FORBIDDEN)

#     videos = Video.objects.filter(course_id=course_id)
#     serializer = VideoSerializer(videos, many=True)
#     return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_subscribed_courses_with_videos(request):
    subscriptions = Subscription.objects.filter(user=request.user).select_related('course')
    
    courses_data = []
    for subscription in subscriptions:
        course = subscription.course
        videos = Video.objects.filter(course=course)
        
        course_data = CourseSerializer(course).data
        course_data['videos'] = VideoSerializer(videos, many=True).data
        courses_data.append(course_data)
    
    return Response(courses_data)