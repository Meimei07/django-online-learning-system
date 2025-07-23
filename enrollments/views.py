from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Enrollment
from courses.models import Course
from .forms import AddEnrollmentForm, UpdateEnrollmentForm, EnrollmentFormInCourse, EnrollmentFormByStudent
from users.models import Student, Instructor
from users.decorators import allow_users

# Create your views here.

@login_required(login_url='users:login')
@allow_users(allow_roles=['admin', 'student'])
def enrollment_list(request):
  enrollments = Enrollment.objects.select_related('student', 'course').all()
  students = Student.objects.all()
  courses = Course.objects.all()
  instructors = Instructor.objects.all()

  selected_student_id = request.GET.get('student')
  if selected_student_id:
    enrollments = enrollments.filter(student_id=selected_student_id)

  selected_courses = request.GET.getlist('course')
  if selected_courses:
    for selected_course in selected_courses:
      enrollments = enrollments.filter(course_id=selected_course)

  selected_instructor_id = request.GET.get('instructor')
  if selected_instructor_id:
    enrollments = enrollments.filter(course__instructor_id=selected_instructor_id)

  context = {
    'enrollments':enrollments,
    'students': students,
    'courses': courses,
    'instructors': instructors,
    'selected_student_id': int(selected_student_id) if selected_student_id else None,
    'selected_courses': [int(t) for t in selected_courses],
    'selected_instructor_id': int(selected_instructor_id) if selected_instructor_id
     else None,
  }

  return render(request, 'enrollments/list.html', context)

@login_required(login_url='users:login')
@allow_users(allow_roles=['admin'])
def enrollment_create(request):
  form = AddEnrollmentForm(request.POST or None)

  if form.is_valid():
    form.save()
    return redirect('enrollments:enrollment_list')
  
  return render(request, 'enrollments/create_update.html', {'form':form})

@login_required(login_url='users:login')
@allow_users(allow_roles=['admin'])
def enrollment_update(request, pk):
  enrollment = Enrollment.objects.filter(pk=pk).first()
  form = UpdateEnrollmentForm(request.POST or None, instance=enrollment)

  if form.is_valid():
    form.save()
    return redirect('enrollments:enrollment_list')
  
  return render(request, 'enrollments/create_update.html', {'form':form})

@login_required(login_url='users:login')
@allow_users(allow_roles=['admin'])
def enrollment_delete(request, pk):
  enrollment = Enrollment.objects.filter(pk=pk).first()

  if request.method == 'POST':
    enrollment.delete()
    return redirect('enrollments:enrollment_list')
  
  return render(request, 'enrollments/delete.html', {'enrollment':enrollment})

@login_required(login_url='users:login')
@allow_users(allow_roles=['admin', 'student'])
def enrollment_create_by_employee(request, pk): # pk of course
  course = Course.objects.filter(pk=pk).first()
  login_user = request.user.groups.first().name

  if login_user == 'admin':
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
  
  else:
    login_id = request.user.student.id
    student = Student.objects.get(pk=login_id)
    form = EnrollmentFormByStudent(initial={'course':course, 'student':student})

    if request.method == 'POST' and 'add-enrollment' in request.POST:
      form = EnrollmentFormByStudent(request.POST or None)

      if form.is_valid():
        if Enrollment.objects.filter(course=course, student=student).exists():
          messages.error(request, "You've enrolled in this course once")
          return redirect('courses:course_detail', pk=course.id)

        print('student enrolls')
        enrollment = form.save(commit=False)
        enrollment.course = course
        enrollment.student = student
        enrollment.save()
        return redirect('courses:course_detail', pk=course.id)
    
    else:
      form = EnrollmentFormByStudent()
    
    return render(request, 'courses/detail.html', {'course':course})


