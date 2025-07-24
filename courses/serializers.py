from rest_framework import serializers
from .models import Course, Module, Video, Subscription, WatchedVideo
from django.contrib.auth.models import User


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['id', 'title', 'url', 'course', 'module']


class ModuleSerializer(serializers.ModelSerializer):
    videos = VideoSerializer(many=True, source='video_set', read_only=True)

    class Meta:
        model = Module
        fields = ['id', 'title', 'course', 'videos']


class CourseSerializer(serializers.ModelSerializer):
    modules = ModuleSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'image', 'duration', 'modules']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class SubscriptionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    course = CourseSerializer(read_only=True)

    class Meta:
        model = Subscription
        fields = ['id', 'user', 'course', 'joined_at', 'completed', 'certificate_issued']


class WatchedVideoSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    video = VideoSerializer(read_only=True)

    class Meta:
        model = WatchedVideo
        fields = ['id', 'user', 'video', 'watched_at']
