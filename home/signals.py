from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Assignment, Review
from .ai_utils import AIAssistant

ai_assistant = AIAssistant()

@receiver([post_save, post_delete], sender=Review)
def invalidate_review_cache(sender, instance, **kwargs):
    ai_assistant.invalidate_cache(instance.assignment.id)

@receiver(post_save, sender=Assignment)
def invalidate_assignment_cache(sender, instance, **kwargs):
    ai_assistant.invalidate_cache(instance.id)
