from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .forms import AssignmentForm, RubricForm
from django.forms import formset_factory
from .models import Assignment, Review
from .ai_utils import AIAssistant
from django.utils import timezone
from datetime import timedelta
from .utils import extract_file_content

def home(request):
    assignments = Assignment.objects.filter(is_published=True).order_by('-date_uploaded')

    search_query = request.GET.get('search', '')
    if search_query:
        assignments = assignments.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(course__icontains=search_query) |
            Q(author__username__icontains=search_query)
        )

    assignment_type = request.GET.get('type', '')
    if assignment_type:
        assignments = assignments.filter(assignment_type=assignment_type)

    course = request.GET.get('course', '')
    if course:
        assignments = assignments.filter(course=course)

    courses = Assignment.objects.values_list('course', flat=True).distinct()

    context = {
        'assignments': assignments,
        'assignment_types': Assignment.TYPE_CHOICES,
        'courses': courses,
        'search_query': search_query,
    }

    return render(request, 'home/home.html', context)

@login_required
def upload_assignment(request):
    if request.method == 'POST':
        assignment_form = AssignmentForm(request.POST, request.FILES)
        if assignment_form.is_valid():
            assignment = assignment_form.save(commit=False)
            assignment.author = request.user

            if 'uploaded_assignment' in request.FILES:
                file = request.FILES['uploaded_assignment']
                assignment.uploaded_assignment = f'assignments/{file.name}'

            assignment.num_criteria = assignment_form.cleaned_data['num_criteria']
            assignment.save()
            return redirect('define_rubric', pk=assignment.pk)
    else:
        assignment_form = AssignmentForm()

    return render(request, 'home/upload_assignment.html', {
        'assignment_form': assignment_form,
    })

@login_required
def define_rubric(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)
    RubricFormSet = formset_factory(RubricForm, extra=assignment.num_criteria)  # type: ignore

    if request.method == 'POST':
        rubric_formset = RubricFormSet(request.POST)
        if rubric_formset.is_valid():
            rubric = {}
            for form in rubric_formset:
                if form.cleaned_data:
                    criterion = form.cleaned_data['criterion']
                    description = form.cleaned_data['description']
                    max_points = form.cleaned_data['max_points']
                    rubric[criterion] = {"description": description, "max_points": max_points}

            assignment.rubric = rubric
            assignment.is_published = True
            assignment.save()
            return redirect('detail', pk=pk)
        else:
            assignment.delete()
            return redirect('upload_assignment')
    else:
        rubric_formset = RubricFormSet()

    return render(request, 'home/define_rubric.html', {
        'assignment': assignment,
        'rubric_formset': rubric_formset,
    })

@login_required
def SubmitReview(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)
    if not assignment.is_published:
        messages.warning(request, 'This assignment is not published yet.')
        return redirect('home')

    rubric_details = []

    if request.method == 'POST':
        rubric_scores = {}
        rubric_description = {}
        total_score = 0
        max_total = 0


        for criterion, details in assignment.rubric.items():
            max_points = details.get('max_points', 0)
            score = int(request.POST.get(criterion, 0))
            rubric_scores[criterion] = score
            rubric_description[criterion] = details.get('description', '')
            total_score += score
            max_total += max_points

        final_percent = (total_score/max_total) * 100 if max_total > 0 else 0
        Review.objects.create(
            assignment = assignment,
            reviewer = request.user,
            rubric_scores = rubric_scores,
            final_percent = final_percent,
            feedback = request.POST.get('feedback'),
            rubric_description = rubric_description
        )
        return redirect('detail', pk = assignment.pk)

    else: #GET REQUEST
        for criterion, details in assignment.rubric.items():
            rubric_details.append({
                'criterion': criterion,
                'description': details.get('description', ''),
                'max_points': details.get('max_points', 0)
            })

    print(rubric_details)
    return render(request, 'home/submit_review.html', {'assignment':assignment, 'rubric_details': rubric_details,})


ai_assistant = AIAssistant()
def DetailView(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)
    if not assignment.is_published:
        messages.warning(request, 'This assignment is not published yet.')
        return redirect('home')

    reviews = assignment.reviews.all() # type: ignore
    rubric_details = []

    content = None
    ai_analysis = None
    if assignment.uploaded_assignment:
        content = extract_file_content(assignment.uploaded_assignment)
        if content and not content.startswith('Error'):
            ai_analysis = ai_assistant.analyze_assignment(
                assignment.title,
                assignment.description,
                content,
                assignment.rubric,
                assignment.id, # type: ignore
            )

    ai_analysis = ai_assistant.analyze_assignment(
        assignment.title,
        assignment.description,
        content,
        assignment.rubric,
        assignment.id, # type: ignore
    )
    if reviews.count() >= 2:
        review_summary = ai_assistant.summarize_reviews(reviews, assignment.id) # type: ignore
    else:
        review_summary = None

    for criterion, details in assignment.rubric.items():
            rubric_details.append({
                'criterion': criterion,
                'description': details.get('description', ''),
                'max_points': details.get('max_points', 0)
            })

    return render(request, 'home/detail.html', {
        'assignment': assignment,
        'reviews': reviews,
        'rubric_details': rubric_details,
        'ai_analysis': ai_analysis,
        'review_summary': review_summary,
    })

def ReviewDetail(request, pk):
    review = get_object_or_404(Review, pk=pk)
    assignment = review.assignment

    rubric_details = []

    for criterion, details in assignment.rubric.items():
            rubric_details.append({
                'criterion': criterion,
                'description': details.get('description', ''),
                'max_points': details.get('max_points', 0),
                'score': review.rubric_scores.get(criterion, 0),
            })

    return render(request, 'home/review_detail.html', {
        'review': review,
        'assignment': assignment,
        'rubric_details': rubric_details,
    })


@login_required
def update_assignment(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)
    if not assignment.is_published:
        messages.warning(request, 'This assignment is not published yet.')
        return redirect('home')

    if request.method == 'POST':
        assignment_form = AssignmentForm(request.POST, request.FILES, instance=assignment)
        assignment_form.fields.pop('num_criteria')
        if assignment_form.is_valid():
            ai_assistant.invalidate_cache(assignment.id) # type: ignore
            updated_assignment = assignment_form.save(commit=False)
            updated_assignment.num_criteria = assignment.num_criteria
            if not request.FILES.get('uploaded_assignment'):
                updated_assignment.uploaded_assignment = assignment.uploaded_assignment
            updated_assignment.save()
            return redirect('detail', pk=pk)
    else:
        assignment_form = AssignmentForm(instance=assignment)
        assignment_form.fields.pop('num_criteria')
    return render(request, 'home/update_assignment.html', {'form': assignment_form})

@login_required
def delete_assignment(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)
    if not assignment.is_published:
        messages.warning(request, 'This assignment is not published yet.')
        return redirect('home')
    if request.method == 'POST':
        assignment.delete()
        return redirect('home')
    return render(request, 'home/delete_assignment.html', {'assignment': assignment})

@login_required
def update_rubric(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)
    if not assignment.is_published:
        messages.warning(request, 'This assignment is not published yet.')
        return redirect('home')

    RubricFormSet = formset_factory(RubricForm, extra=0) # type: ignore

    if request.method == 'POST':
        rubric_formset = RubricFormSet(request.POST)
        if rubric_formset.is_valid():
            rubric = {}
            for form, (old_criterion, old_details) in zip(rubric_formset, assignment.rubric.items()):
                if form.cleaned_data:
                    criterion = form.cleaned_data['criterion']
                    description = form.cleaned_data['description']
                    max_points = old_details['max_points']
                    rubric[criterion] = {
                        "description": description,
                        "max_points": max_points
                    }

            assignment.rubric = rubric
            assignment.save()
            return redirect('detail', pk=pk)
    else:
        initial_data = [
            {
                'criterion': criterion,
                'description': details['description'],
                'max_points': details['max_points']
            }
            for criterion, details in assignment.rubric.items()
        ]
        rubric_formset = RubricFormSet(initial=initial_data) # type: ignore

    return render(request, 'home/update_rubric.html', {
        'assignment': assignment,
        'rubric_formset': rubric_formset
    })

@login_required
def update_review(request, pk):
    review = get_object_or_404(Review, pk=pk)
    assignment = review.assignment
    rubric_details = []

    if request.method == 'POST':
        rubric_scores = {}
        total_score = 0
        max_total = 0

        for criterion, details in assignment.rubric.items():
            max_points = details.get('max_points', 0)
            score = int(request.POST.get(criterion, 0))
            rubric_scores[criterion] = score
            total_score += score
            max_total += max_points

        final_percent = (total_score/max_total) * 100 if max_total > 0 else 0

        review.rubric_scores = rubric_scores
        review.final_percent = final_percent
        review.feedback = request.POST.get('feedback')
        review.save()

        return redirect('review_detail', pk=pk)

    else:
        for criterion, details in assignment.rubric.items():
            rubric_details.append({
                'criterion': criterion,
                'description': details.get('description', ''),
                'max_points': details.get('max_points', 0),
                'score': review.rubric_scores.get(criterion, 0)
            })

    return render(request, 'home/update_review.html', {
        'review': review,
        'assignment': assignment,
        'rubric_details': rubric_details
    })

@login_required
def delete_review(request, pk):
    review = get_object_or_404(Review, pk=pk)
    assignment_pk = review.assignment.pk
    if request.method == 'POST':
        review.delete()
        return redirect('detail', pk=assignment_pk)
    return render(request, 'home/delete_review.html', {'review': review})
