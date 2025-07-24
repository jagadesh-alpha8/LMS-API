from rest_framework import serializers
from .models import Assessment, Question, UserAssessmentSubmission, UserAnswer


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'


class AssessmentSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Assessment
        fields = ['id', 'title', 'description', 'course', 'total_marks', 'created_at', 'questions']


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
            UserAnswer.objects.create(submission=submission, question=question, selected_option=selected, is_correct=is_correct)

        submission.score = score
        submission.save()
        return submission
