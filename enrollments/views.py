from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Enrollment
from courses.models import Course
from .forms import EnrollmentForm, EnrollmentFormInCourse

# Create your views here.
def enrollment_list(request):
  enrollments = Enrollment.objects.select_related('student', 'course').all()
  return render(request, 'enrollments/list.html', {'enrollments':enrollments})

def enrollment_create(request):
  form = EnrollmentForm(request.POST or None)

  if form.is_valid():
    form.save()
    return redirect('enrollments:enrollment_list')
  
  return render(request, 'enrollments/create_update.html', {'form':form})

def enrollment_update(request, pk):
  enrollment = Enrollment.objects.filter(pk=pk).first()
  form = EnrollmentForm(request.POST or None, instance=enrollment)

  if form.is_valid():
    form.save()
    return redirect('enrollments:enrollment_list')
  
  return render(request, 'enrollments/create_update.html', {'form':form})

def enrollment_delete(request, pk):
  enrollment = Enrollment.objects.filter(pk=pk).first()

  if request.method == 'POST':
    enrollment.delete()
    return redirect('enrollments:enrollment_list')
  
  return render(request, 'enrollments/delete.html', {'enrollment':enrollment})

def enrollment_create_by_employee(request, pk): # pk of course
  course = Course.objects.filter(pk=pk).first()
  form = EnrollmentFormInCourse(initial={'course':course})

  if request.method == 'POST':
    form = EnrollmentFormInCourse(request.POST or None)
    student = request.POST.get('student')

    if form.is_valid():
      if Enrollment.objects.filter(course=course, student=student).exists():
        messages.error(request, "The enrollment with this student and course already exists.")
        return render(request, 'enrollments/create_update_by_employee.html', {'form':form, 'course': course, 'student':student})
      
      enrollment = form.save(commit=False)
      enrollment.course = course
      enrollment.save()
      return redirect('courses:course_list')   
  else:
    form = EnrollmentFormInCourse()
    
  return render(request, 'enrollments/create_update_by_employee.html', {'form':form, 'course':course})
