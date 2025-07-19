from django.shortcuts import render
from users.models import Employee, Instructor, Student
from courses.models import Course
from enrollments.models import Enrollment

# Create your views here.
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
