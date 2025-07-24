from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Review
from .forms import ReviewForm

from courses.models import Course
from users.models import Student
from users.decorators import admin_only, allow_users

# Create your views here.

@login_required(login_url='users:login')
@admin_only
def review_list(request):
  reviews = Review.objects.select_related('student', 'course')
  students = Student.objects.all()
  courses = Course.objects.all()
  stars = ['5', '4', '3', '2', '1']

  selected_student_id = request.GET.get('student')
  if selected_student_id:
    reviews = reviews.filter(student=selected_student_id)

  selected_course_id = request.GET.get('course')
  if selected_course_id:
    reviews = reviews.filter(course=selected_course_id)

  selected_star = request.GET.get('star')
  if selected_star:
    reviews = reviews.filter(star=selected_star)

  context = {
    'reviews': reviews,
    'students': students,
    'courses': courses,
    'stars': stars,
    'selected_student_id': int(selected_student_id) if selected_student_id else None,
    'selected_course_id': int(selected_course_id) if selected_course_id else None,
    'selected_star': selected_star,
  }

  return render(request, 'reviews/list.html', context)

@login_required(login_url='users:login')
@allow_users(allow_roles=['student'])
def review_create(request, pk): # pk of course
  login_id = request.user.student.id
  
  student = Student.objects.get(pk=login_id)
  course = Course.objects.get(pk=pk)

  form = ReviewForm(initial={'student':student, 'course':course})

  if Review.objects.filter(student=student, course=course).exists():
    messages.error(request, "Reviewed already")
    print('messages: ',messages)
    return redirect('courses:course_detail', pk=course.id)
  else:
    if request.method == 'POST':
      form = ReviewForm(request.POST or None)

      if form.is_valid():
        review = form.save(commit=False)
        review.student = student
        review.course = course
        review.save()
        return redirect('courses:course_detail', pk=course.id)
      
    else:
      form = ReviewForm(initial={'student':student, 'course':course})

  return render(request, 'reviews/create.html', {'form':form, 'course':course})
