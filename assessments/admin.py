from django.contrib import admin
from .models import Assessment, Question, UserAssessmentSubmission, UserAnswer, UserWatchedVideo

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1

@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'created_at']
    inlines = [QuestionInline]

admin.site.register(Question)
admin.site.register(UserAssessmentSubmission)
admin.site.register(UserAnswer)
admin.site.register(UserWatchedVideo)
