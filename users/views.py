from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterationForm
from home.models import Assignment, Review

# Create your views here.
def register_view(request):
    if request.method == 'POST':
        form = UserRegisterationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegisterationForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return render(request, 'users/logout.html')

@login_required
def dashboard(request):
    assignments = Assignment.objects.filter(author = request.user)
    assignments = assignments.filter(is_published=True)

    reviews = Review.objects.filter(reviewer = request.user)

    stats = {
        'num_assignments': len(assignments),
        'num_reviews': len(reviews),
    }

    return render(request, 'users/dashboard.html', {
        'assignments': assignments,
        'reviews': reviews,
        'stats': stats,
    })
