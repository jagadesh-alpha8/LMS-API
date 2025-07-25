# from rest_framework import serializers
# from .models import *
# from courses.models import Course


# class QuestionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Question
#         fields = [
#             'id', 'question_text',
#             'option_a', 'option_b', 'option_c', 'option_d',
#             'correct_option'
#         ]


# class AssessmentWithQuestionsSerializer(serializers.ModelSerializer):
#     course_id = serializers.PrimaryKeyRelatedField(
#         queryset=Course.objects.all(), source='course'
#     )
#     questions = QuestionSerializer(many=True, read_only=True)

#     class Meta:
#         model = Assessment
#         fields = [
#             'id', 'course_id', 'title', 'description',
#             'total_marks', 'created_at', 'questions'
#         ]
#         read_only_fields = ['created_at']


# # 3. UserAnswer Serializer (for recording submission answers)
# class UserAnswerSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserAnswer
#         fields = ['question', 'selected_option', 'is_correct']


# # 4. Submission Serializer (optional: for showing past submissions)
# class UserAssessmentSubmissionSerializer(serializers.ModelSerializer):
#     answers = UserAnswerSerializer(many=True, source='useranswer_set', read_only=True)

#     class Meta:
#         model = UserAssessmentSubmission
#         fields = ['id', 'user', 'assessment', 'attempt_number', 'score', 'submitted_at', 'answers']
#         read_only_fields = ['user', 'assessment', 'attempt_number', 'submitted_at']


from rest_framework import serializers
from .models import Question, Assessment, UserAnswer, UserAssessmentSubmission
from courses.models import Course


class QuestionSerializer(serializers.ModelSerializer):
    selected_option = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = [
            'id', 'question_text',
            'option_a', 'option_b', 'option_c', 'option_d',
            'correct_option',  # Remove this if you don't want students to see correct answers
            'selected_option',
        ]

    def get_selected_option(self, obj):
        user = self.context.get('user')
        if not user:
            return None

        assessment = obj.assessment
        submission = UserAssessmentSubmission.objects.filter(
            user=user, assessment=assessment
        ).order_by('-attempt_number').first()

        if not submission:
            return None

        answer = UserAnswer.objects.filter(submission=submission, question=obj).first()
        return answer.selected_option if answer else None


class AssessmentWithQuestionsSerializer(serializers.ModelSerializer):
    course_id = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all(), source='course'
    )
    questions = serializers.SerializerMethodField()

    class Meta:
        model = Assessment
        fields = [
            'id', 'course_id', 'title', 'description',
            'total_marks', 'created_at', 'questions'
        ]
        read_only_fields = ['created_at']

    def get_questions(self, obj):
        return QuestionSerializer(
            obj.questions.all(), many=True, context=self.context
        ).data


class UserAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAnswer
        fields = ['question', 'selected_option', 'is_correct']


class UserAssessmentSubmissionSerializer(serializers.ModelSerializer):
    answers = UserAnswerSerializer(many=True, source='useranswer_set', read_only=True)

    class Meta:
        model = UserAssessmentSubmission
        fields = ['id', 'user', 'assessment', 'attempt_number', 'score', 'submitted_at', 'answers']
        read_only_fields = ['user', 'assessment', 'attempt_number', 'submitted_at']
