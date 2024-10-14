from django.shortcuts import render, redirect
from .forms import EventForm
from django.contrib.auth.decorators import login_required
from django.views.generic import *
import os

# Create your views here.
class HomeView(TemplateView):
  template_name = 'home/home.html'

@login_required
def create_event(request):
  if request.method == 'POST':
    form = EventForm(request.POST)
    if form.is_valid():
      event = form.save(commit=False)
      event.host = request.user
      return redirect('home')

  else:
    form = EventForm()

  return render(request, 'home/create_event.html', {'form': form})
