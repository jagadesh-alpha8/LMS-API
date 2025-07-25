
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from courses.models import Subscription, Course
from assessments.models import Assessment, Question, UserAssessmentSubmission, UserAnswer
from assessments.serializers import AssessmentWithQuestionsSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def subscribed_assessments_with_questions(request):
    """
    Return all assessments with questions and user's selected options for subscribed courses.
    """
    # Get course IDs user subscribed to
    subscribed_course_ids = Subscription.objects.filter(
        user=request.user
    ).values_list('course_id', flat=True)

    # Get assessments for those courses
    assessments = Assessment.objects.filter(    
        course_id__in=subscribed_course_ids
    ).prefetch_related('questions')

    # Pass user in context to get selected_option per question
    serializer = AssessmentWithQuestionsSerializer(
        assessments, many=True, context={'user': request.user}
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_assessment(request):
    """
    Accept user's assessment submission.
    Expected JSON format:
    {
        "course_id": 1,
        "answers": [
            {"question": 10, "selected_option": "B"},
            {"question": 11, "selected_option": "C"}
        ]
    }
    """
    user = request.user
    data = request.data
    course_id = data.get('course_id')
    answers_data = data.get('answers', [])

    if not course_id or not answers_data:
        return Response({"detail": "course_id and answers are required."}, status=400)

    try:
        # Assume one assessment per course
        assessment = Assessment.objects.get(course_id=course_id)
    except Assessment.DoesNotExist:
        return Response({"detail": "Assessment for this course not found."}, status=404)

    # Count user's previous attempts
    previous_attempts = UserAssessmentSubmission.objects.filter(user=user, assessment=assessment).count()
    attempt_number = previous_attempts + 1

    # Create a new submission
    submission = UserAssessmentSubmission.objects.create(
        user=user,
        assessment=assessment,
        attempt_number=attempt_number
    )

    correct_count = 0
    total_questions = len(answers_data)

    for ans in answers_data:
        try:
            question = Question.objects.get(id=ans['question'], assessment=assessment)
        except Question.DoesNotExist:
            continue  # Skip invalid question IDs

        selected = ans.get('selected_option')
        is_correct = (selected == question.correct_option)

        if is_correct:
            correct_count += 1

        # Store each answer
        UserAnswer.objects.create(
            submission=submission,
            question=question,
            selected_option=selected,
            is_correct=is_correct
        )

    # Calculate score based on total marks
    score = (correct_count / total_questions) * assessment.total_marks if total_questions else 0
    submission.score = score
    submission.save()

    return Response({
        "message": "Assessment submitted successfully.",
        "score": score,
        "attempt_number": attempt_number
    }, status=status.HTTP_201_CREATED)
