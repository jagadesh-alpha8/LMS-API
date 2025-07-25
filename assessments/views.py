from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from courses.models import *
from assessments.models import *
from assessments.serializers import *


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def subscribed_assessments_with_questions(request):
    # Get the list of course IDs subscribed by the user
    subscribed_course_ids = Subscription.objects.filter(user=request.user).values_list('course_id', flat=True)

    # Fetch all assessments related to those courses
    assessments = Assessment.objects.filter(course_id__in=subscribed_course_ids).prefetch_related('questions')

    # Serialize and return
    serializer = AssessmentWithQuestionsSerializer(assessments, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)




# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def submit_assessment_answers(request, course_id, assessment_id):
#     user = request.user

#     # Check if user is subscribed to the course
#     if not Subscription.objects.filter(user=user, course_id=course_id).exists():
#         return Response({'detail': 'User not subscribed to this course.'}, status=status.HTTP_403_FORBIDDEN)

#     # Validate assessment
#     try:
#         assessment = Assessment.objects.get(id=assessment_id, course_id=course_id)
#     except Assessment.DoesNotExist:
#         return Response({'detail': 'Assessment not found.'}, status=status.HTTP_404_NOT_FOUND)

#     submitted_answers = request.data.get('answers', [])

#     if not submitted_answers:
#         return Response({'detail': 'No answers submitted.'}, status=status.HTTP_400_BAD_REQUEST)

#     # Count previous attempts
#     attempt_number = (
#         UserAssessmentSubmission.objects.filter(user=user, assessment=assessment).count() + 1
#     )

#     total_correct = 0
#     submission = UserAssessmentSubmission.objects.create(
#         user=user,
#         assessment=assessment,
#         attempt_number=attempt_number
#     )

#     for ans in submitted_answers:
#         try:
#             question = Question.objects.get(id=ans['question'], assessment=assessment)
#         except Question.DoesNotExist:
#             continue

#         selected_option = ans.get('selected_option')
#         is_correct = (selected_option == question.correct_option)
#         if is_correct:
#             total_correct += 1

#         UserAnswer.objects.create(
#             submission=submission,
#             question=question,
#             selected_option=selected_option,
#             is_correct=is_correct
#         )

#     # Assume 1 mark per correct answer
#     submission.score = total_correct
#     submission.save()

#     return Response({
#         'detail': 'Assessment submitted successfully.',
#         'score': submission.score,
#         'total_questions': assessment.questions.count(),
#         'attempt_number': submission.attempt_number
#     }, status=status.HTTP_200_OK)
