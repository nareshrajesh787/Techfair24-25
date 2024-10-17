from typing import List
from django.shortcuts import render, redirect
from .forms import EventForm
from django.contrib.auth.decorators import login_required
from django.views.generic import *
from .models import Event
import os

# Create your views here.
class HomeView(ListView):
  model = Event
  template_name = 'home/home.html'
  context_object_name = "events"
  ordering = ['-event_date']
  paginate_by = 7

@login_required
def create_event(request):
  if request.method == 'POST':
    form = EventForm(request.POST)
    if form.is_valid():
      event = form.save(commit=False)
      event.host = request.user
      event.save()
      return redirect('home')

  else:
    form = EventForm()

  return render(request, 'home/create_event.html', {'form': form})
