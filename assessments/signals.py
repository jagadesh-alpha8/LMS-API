from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserAssessmentSubmission

@receiver(post_save, sender=UserAssessmentSubmission)
def update_certificate_status(sender, instance, created, **kwargs):
    if created:
        print(f"Assessment submitted by {instance.user.username}")
