from typing import List
from django.shortcuts import render, redirect
from .forms import EventForm
from django.contrib.auth.decorators import login_required
from django.views.generic import *
from django.utils import timezone
from .models import Event
import os
import operator
from functools import reduce
from django.db.models import Q



# Create your views here.
class HomeView(ListView):
    model = Event
    template_name = 'home/home.html'
    context_object_name = 'events'
    ordering = ['-event_date']

    def get_queryset(self):
        queryset = super().get_queryset()
        show_past = self.request.GET.get('show_past') == 'true'
        event_type_filter = self.request.GET.get('event_type')
        search_query = self.request.GET.get('search', '')

        if not show_past:
            queryset = queryset.filter(event_date__gte=timezone.now())

        if event_type_filter and event_type_filter != 'All':
            queryset = queryset.filter(event_type=event_type_filter)

        if search_query:
            queryset = queryset.filter(
                Q(event_name__icontains=search_query) |
                Q(event_description__icontains=search_query)
            )


        return queryset


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['show_past'] = self.request.GET.get('show_past') == 'true'
        context['selected_event_type'] = self.request.GET.get('event_type', '')
        context['search_query'] = self.request.GET.get('search', '')
        return context

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
