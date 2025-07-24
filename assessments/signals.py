from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import StudentAssessment
from courses.models import Subscription
from django.db import transaction


@receiver(post_save, sender=StudentAssessment)
def update_user_score(sender, instance, **kwargs):
    try:
        with transaction.atomic():
            subscription, created = Subscription.objects.get_or_create(
                user=instance.user,
                course=instance.course,
                defaults={"origin": 0}
            )

            # Sum all correct answers across attempts
            all_assessments = StudentAssessment.objects.filter(
                user=instance.user,
                course=instance.course
            )

            total_score = sum(a.correct_answers for a in all_assessments)
            subscription.online_score = total_score
            subscription.save()
    except Exception as e:
        print("Progress update failed:", e)
