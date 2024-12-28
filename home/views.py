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
    avg_rating = reviews.aggregate(models.Avg('rating'))['rating_avg'] or 0

    return render(request, 'home/detail.html', {
        'assignment': assignment,
        'reviews': reviews,
        'avg_rating': avg_rating
    })

def SubmitReview(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)

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
        'form': form
    })
