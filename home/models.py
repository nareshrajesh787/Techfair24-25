from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
event_options = (
        ('SPORTS', 'Sports'),
        ('ACADEMIC', 'Academic'),
        ('CULTURAL', 'Cultural'),
        ('CELEBRATION', 'Celebration')
    )

class Event(models.Model):
    event_name = models.CharField(max_length=100)
    event_description = models.TextField(max_length=500)
    event_date = models.DateTimeField()
    event_type = models.CharField(max_length=30,choices=event_options)
    date_posted = models.DateTimeField(default=timezone.now)
    host = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.event_name
