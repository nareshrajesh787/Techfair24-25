from django import forms
from .models import Assignment, Review

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = [
            'title', 'description', 'course',
            'assignment_type', 'uploaded_assignment', 'uploaded_rubric'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'course': forms.TextInput(attrs={'placeholder': 'What is it for (eg. AP Lang, Science Fair, etc.)'}),
            'assignment_type': forms.Select(choices=Assignment.TYPE_CHOICES),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = [
            'feedback', 'rating'
        ]
        widgets = {
            'feedback': forms.Textarea(attrs={'rows': 5}),
            'rating': forms.RadioSelect(choices=[(i, f"{i} Star{'s' if i > 1 else ''}") for i in range(1,6)])
        }
