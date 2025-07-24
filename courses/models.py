from django.db import models
from django.contrib.auth.models import User


class Course(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='courses/', null=True, blank=True)
    duration = models.IntegerField(default=0)  # in minutes

    def __str__(self):
        return self.name


class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.course.name} - {self.title}"



class Video(models.Model):
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    module = models.ForeignKey('Module', on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=200)
    youtube_id = models.CharField(max_length=20)

    @property
    def video_url(self):
        return f"https://www.youtube.com/watch?v={self.youtube_id}"

    def __str__(self):
        return self.title



class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    certificate_issued = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} → {self.course.name}"
