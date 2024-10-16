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
  paginate_by = 10

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["now"] = timezone.now()
    return context

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
