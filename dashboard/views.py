from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from users.models import Employee, Instructor, Student
from users.decorators import allow_users, admin_only
from courses.models import Course
from enrollments.models import Enrollment

# Create your views here.

@login_required(login_url='users:login')
@admin_only
def dashboard_view(request):
  total_instructors = Instructor.objects.count()
  total_students = Student.objects.count()
  total_courses = Course.objects.count()
  total_enrollments = Enrollment.objects.count()

  instructors = Instructor.objects.all()
  students = Student.objects.all()

  context = {
    'instructors': instructors,
    'students': students,
    'total_instructors': total_instructors,
    'total_students': total_students,
    'total_courses': total_courses,
    'total_enrollments': total_enrollments,
  }

  return render(request, 'dashboard/home.html', context)

def instructor_dashboard_view(request):
  login_id = request.user.instructor.id
  instructor = Instructor.objects.get(pk=login_id)

  if instructor is not None:
    courses = instructor.courses.all()

  total_enrollments = []

  for course in courses:
    enrollments = Enrollment.objects.filter(course=course)

    for enrollment in enrollments:
      total_enrollments.append(enrollment)
  
  print("enroll: ", total_enrollments)
  
  context = {
    'courses': courses,
    'enrollments': total_enrollments,
  }

  return render(request, 'dashboard/instructor_dashboard.html', context)

def student_dashboard_view(request):
  login_id = request.user.student.id
  student = Student.objects.get(pk=login_id)

  enrollments = None
  total_progress = 0
  total_completed = 0

  if student is not None:
    enrollments = student.enrollments.all()

    for enrollment in enrollments:
      if enrollment.status == 'Progress':
        total_progress += 1
      elif enrollment.status == 'Completed':
        total_completed += 1

  context = {
    'enrollments': enrollments,
    'total_progress': total_progress,
    'total_completed': total_completed,
  }

  return render(request, 'dashboard/student_dashboard.html', context)
