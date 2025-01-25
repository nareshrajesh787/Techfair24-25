from cProfile import label
from django import forms
from .models import Assignment, Review

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = [
            'title', 'description', 'course',
            'assignment_type', 'uploaded_assignment' ,'num_criteria'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'course': forms.TextInput(attrs={'placeholder': 'What is it for (eg. AP Lang, Science Fair, etc.)'}),
            'assignment_type': forms.Select(choices=Assignment.TYPE_CHOICES),
            'num_criteria': forms.NumberInput(attrs={'min': 1, 'max': 10}),
        }
        labels = {
            'num_criteria': 'Number of Rubric Criteria',
            'uploaded_assignment': 'Upload Assignment File',
        }

class RubricForm(forms.Form):
    criterion = forms.CharField(max_length=50, label="Criterion Name")
    description = forms.CharField(max_length=200, label="Criterion Description")
    max_points = forms.IntegerField(label="Maximum Points Available")
