from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['event_name', 'event_description', 'event_date', 'event_type']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Event Name'}),
            'event_description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Event Description', 'rows': 3}),
            'event_date': forms.DateTimeInput(attrs={ 'class':'form-control', 'type': 'datetime-local'}),
            'event_type': forms.Select(attrs={'class': 'form-control'})
        }
