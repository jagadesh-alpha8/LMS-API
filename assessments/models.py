from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from courses.models import Course, Video, Subscription
from django.contrib.auth.models import User  # or from users.models import User if you use custom user


class Assessment(models.Model):
    name = models.CharField(max_length=255)
    serial = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name


class AssessmentQuestion(models.Model):
    CORRECT_OPTIONS = (
        (1, 'Option 1'),
        (2, 'Option 2'),
        (3, 'Option 3'),
        (4, 'Option 4'),
    )
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE)
    question = models.TextField()
    option_1 = models.TextField()
    option_2 = models.TextField()
    option_3 = models.TextField()
    option_4 = models.TextField()
    correct_answer = models.IntegerField(choices=CORRECT_OPTIONS)

    def __str__(self):
        return self.question


class StudentAssessment(models.Model):
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    course_video = models.ForeignKey(Video, on_delete=models.SET_NULL, null=True, blank=True)

    total_questions = models.IntegerField(default=0)
    correct_answers = models.IntegerField(default=0)
    attempt = models.IntegerField(default=1)
    data = models.JSONField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.assessment.name}"
