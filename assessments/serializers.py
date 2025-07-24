from rest_framework import serializers
from .models import Assessment, Question, UserAssessmentSubmission, UserAnswer

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'

class AssessmentSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    is_eligible = serializers.SerializerMethodField()

    class Meta:
        model = Assessment
        fields = ['id', 'title', 'description', 'course', 'total_marks', 'created_at', 'questions', 'is_eligible']

    def get_is_eligible(self, obj):
        user = self.context['request'].user
        if not user.is_authenticated:
            return False
        total = obj.course.video_set.count()
        watched = obj.course.video_set.filter(userwatchedvideo__user=user).count()
        return total > 0 and total == watched

class UserAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAnswer
        fields = ['question', 'selected_option']

class UserAssessmentSubmissionSerializer(serializers.ModelSerializer):
    answers = UserAnswerSerializer(many=True)
    assessment = serializers.PrimaryKeyRelatedField(queryset=Assessment.objects.all())

    class Meta:
        model = UserAssessmentSubmission
        fields = ['assessment', 'answers', 'score', 'attempt_number']

    def create(self, validated_data):
        user = self.context['request'].user
        answers_data = validated_data.pop('answers')
        assessment = validated_data['assessment']

        # ✅ Check video completion
        total_videos = assessment.course.video_set.count()
        watched = assessment.course.video_set.filter(userwatchedvideo__user=user).count()
        if total_videos == 0 or watched < total_videos:
            raise serializers.ValidationError("Watch all course videos before submitting the assessment.")

        # attempt logic
        last_attempt = UserAssessmentSubmission.objects.filter(user=user, assessment=assessment).order_by('-attempt_number').first()
        attempt_number = 1 if not last_attempt else last_attempt.attempt_number + 1

        submission = UserAssessmentSubmission.objects.create(user=user, assessment=assessment, attempt_number=attempt_number)

        score = 0
        for answer_data in answers_data:
            question = answer_data['question']
            selected = answer_data['selected_option']
            is_correct = (selected == question.correct_option)
            if is_correct:
                score += 1
            UserAnswer.objects.create(
                submission=submission,
                question=question,
                selected_option=selected,
                is_correct=is_correct
            )

        submission.score = score
        submission.save()
        return submission
