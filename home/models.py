from django.db import models
from django.contrib.auth.models import User

class Assignment(models.Model):
    TYPE_CHOICES = [
        ('Essay', 'Essay'),
        ('Lab Report', 'Lab Report'),
        ('Presentation', 'Presentation'),
        ('Narrative', 'Narrative')
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    course = models.CharField(max_length=100)
    assignment_type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    uploaded_assignment = models.FileField(upload_to='assignments/')
    uploaded_rubric = models.FileField(upload_to='rubrics/', blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_uploaded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Review(models.Model):
    assignment = models.ForeignKey(Assignment, related_name="reviews", on_delete=models.CASCADE)
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    feedback = models.TextField()
    date_reviewed = models.DateTimeField(auto_now_add=True)
    rating = models.PositiveSmallIntegerField(choices=[(i, f"{i} Star{'s' if i > 1 else ''}") for i in range(1,6)])

    def __str__(self):
        return f"{self.reviewer.username} - {self.rating} stars"
