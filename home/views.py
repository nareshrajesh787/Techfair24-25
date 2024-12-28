from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Avg
from django.contrib.auth.decorators import login_required
from .forms import AssignmentForm, ReviewForm
from .models import Assignment, Review

@login_required
def upload_assignment(request):
    if request.method == 'POST':
        form = AssignmentForm(request.POST, request.FILES)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.author = request.user
            assignment.save()
            return redirect('home')
    else:
        form = AssignmentForm()
    return render(request, 'home/upload_assignment.html', {'form': form})

def assignment_list(request):
    assignments = Assignment.objects.all().order_by('-date_uploaded')
    return render(request, 'home/home.html', {'assignments': assignments})

def DetailView(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)
    reviews = assignment.reviews.all()
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0

    star_range = range(5)

    return render(request, 'home/detail.html', {
        'assignment': assignment,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'star_range': star_range
    })

def SubmitReview(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)

    star_range = range(5)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.assignment = assignment
            review.reviewer = request.user
            review.save()
            return redirect('detail', assignment.pk)
    else:
        form = ReviewForm()

    return render(request, 'home/submit_review.html', {
        'assignment' : assignment,
        'star_range' : star_range,
        'form': form
    })
