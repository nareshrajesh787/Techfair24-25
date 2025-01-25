from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator

class Assignment(models.Model):
    TYPE_CHOICES = [
        ('Essay', 'Essay'),
        ('Lab Report', 'Lab Report'),
        ('Presentation', 'Presentation'),
        ('Narrative', 'Narrative'),
        ('Classwork', 'Classwork'),
        ('Project', 'Project'),
        ('Other', 'Other'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    course = models.CharField(max_length=100)
    assignment_type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    uploaded_assignment = models.FileField(upload_to='assignments/')
    num_criteria = models.PositiveSmallIntegerField(validators=[MaxValueValidator(12)], default=4)
    rubric = models.JSONField(default=dict)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_uploaded = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Review(models.Model):
    assignment = models.ForeignKey(Assignment, related_name="reviews", on_delete=models.CASCADE)
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    feedback = models.TextField()
    rubric_scores = models.JSONField(default=dict)
    rubric_description = models.JSONField(default=dict)
    final_percent = models.FloatField()
    date_reviewed = models.DateTimeField(auto_now_add=True)
    rating = models.PositiveSmallIntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.assignment.title} reviewed by {self.reviewer.username}"
