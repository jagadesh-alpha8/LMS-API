from django.db import models
from django.contrib.auth.models import User
from courses.models import Course, Video


class Assessment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assessments')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    total_marks = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.course.name} - {self.title}"


class Question(models.Model):
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    correct_option = models.CharField(
        max_length=1,
        choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')]
    )

    def __str__(self):
        return self.question_text[:60]


class UserWatchedVideo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    watched_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'video')


class UserAssessmentSubmission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True)
    score = models.FloatField(default=0.0)
    attempt_number = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.user.username} - {self.assessment.title} - Attempt {self.attempt_number}"


class UserAnswer(models.Model):
    submission = models.ForeignKey(UserAssessmentSubmission, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.CharField(max_length=1, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')])
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.submission.user.username} - Q{self.question.id} - {self.selected_option}"
