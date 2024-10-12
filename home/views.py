from django.shortcuts import render
from django.views.generic import TemplateView
import os

# Create your views here.

class HomeView(TemplateView):
  template_name = 'home/home.html'
