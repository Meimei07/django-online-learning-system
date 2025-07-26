from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required

from .models import Employee, Instructor, Student
from .forms import EmployeeForm, InstructorForm, StudentForm, CustomUserForm
from .decorators import allow_users

# Create your views here.

#Employee

@login_required(login_url='login')
@allow_users(allow_roles=['admin'])
def List(request):
  employees = Employee.objects.all()
  return render(request, 'employees/list.html', {'employees':employees})

@login_required(login_url='login')
@allow_users(allow_roles=['admin'])
def Create(request):
  if request.method == 'POST':
    employee_form = EmployeeForm(request.POST or None)
    user_form = CustomUserForm(request.POST or None)

    if employee_form.is_valid() and user_form.is_valid():
      user = user_form.save()

      group = Group.objects.get(name='admin')
      user.groups.add(group)

      employee = employee_form.save(commit=False)
      employee.user = user
      employee.save()
      return redirect('users:employee_list')
  else:
    employee_form = EmployeeForm()
    user_form = CustomUserForm()
  
  return render(request, 'employees/create_update.html', {'employee_form':employee_form, 'user_form':user_form})

@login_required(login_url='login')
@allow_users(allow_roles=['admin'])
def Update(request, pk):
  employee = Employee.objects.filter(pk=pk).first()
  employee_form = EmployeeForm(request.POST or None, instance=employee)

  if employee_form.is_valid():
    employee_form.save()
    return redirect('users:employee_list')

  return render(request, 'employees/create_update.html', {'employee_form':employee_form})

@login_required(login_url='login')
@allow_users(allow_roles=['admin'])
def Delete(request, pk):
  employee = Employee.objects.filter(pk=pk).first()
  user = employee.user

  if request.method == 'POST':
    employee.delete()
    user.delete()
    return redirect('users:employee_list')
  
  return render(request, 'employees/delete.html', {'employee':employee})

#Instructor

@login_required(login_url='login')
@allow_users(allow_roles=['admin'])
def Instructor_List(request):
  instructors = Instructor.objects.all()
  return render(request, 'instructors/list.html', {'instructors':instructors})

@login_required(login_url='login')
@allow_users(allow_roles=['admin'])
def Instructor_Create(request):
  if request.method == 'POST':
    instructor_form = InstructorForm(request.POST or None)
    user_form = CustomUserForm(request.POST or None)

    if instructor_form.is_valid() and user_form.is_valid():
      user = user_form.save()

      group = Group.objects.get(name='instructor')
      user.groups.add(group)

      instructor = instructor_form.save(commit=False)
      instructor.user = user
      instructor.save()
      return redirect('users:instructor_list')
  
  else:
    instructor_form = InstructorForm()
    user_form = CustomUserForm()
  
  return render(request, 'instructors/create_update.html', {'instructor_form':instructor_form, 'user_form':user_form})

@login_required(login_url='login')
@allow_users(allow_roles=['admin'])
def Instructor_Update(request, pk):
  instructor = Instructor.objects.filter(pk=pk).first()
  instructor_form = InstructorForm(request.POST or None, instance=instructor)

  if instructor_form.is_valid():
    instructor_form.save()
    return redirect('users:instructor_list')

  return render(request, 'instructors/create_update.html', {'instructor_form':instructor_form})

@login_required(login_url='login')
@allow_users(allow_roles=['admin'])
def Instructor_Delete(request, pk):
  instructor = Instructor.objects.filter(pk=pk).first()
  user = instructor.user

  if request.method == 'POST':
    instructor.delete()
    user.delete()
    return redirect('users:instructor_list')
  
  return render(request, 'instructors/delete.html', {'instructor':instructor})

@login_required(login_url='login')
@allow_users(allow_roles=['admin'])
def Instructor_Detail(request, pk):
  instructor = Instructor.objects.filter(pk=pk).first()
  return render(request, 'instructors/detail.html', {'instructor':instructor})

#Student

@login_required(login_url='login')
@allow_users(allow_roles=['admin'])
def Student_List(request):
  students = Student.objects.all()
  return render(request, 'students/list.html', {'students':students})

@login_required(login_url='login')
@allow_users(allow_roles=['admin'])
def Student_Create(request):
  if request.method == 'POST':
    student_form = StudentForm(request.POST or None)
    user_form = CustomUserForm(request.POST or None)

    if student_form.is_valid() and user_form.is_valid():
      user = user_form.save()

      group = Group.objects.get(name='student')
      user.groups.add(group)

      student = student_form.save(commit=False)
      student.user = user
      student.save()
      return redirect('users:student_list')
    
  else:
    student_form = StudentForm()
    user_form = CustomUserForm()
  
  return render(request, 'students/create_update.html', {'student_form':student_form, 'user_form':user_form})

@login_required(login_url='login')
@allow_users(allow_roles=['admin'])
def Student_Update(request, pk):
  student = Student.objects.filter(pk=pk).first()
  student_form = StudentForm(request.POST or None, instance=student)

  if student_form.is_valid():
    student_form.save()
    return redirect('users:student_list')

  return render(request, 'students/create_update.html', {'student_form':student_form})

@login_required(login_url='login')
@allow_users(allow_roles=['admin'])
def Student_Delete(request, pk):
  student = Student.objects.filter(pk=pk).first()
  user = student.user

  if request.method == 'POST':
    student.delete()
    user.delete()
    return redirect('users:student_list')
  
  return render(request, 'students/delete.html', {'student':student})

@login_required(login_url='login')
@allow_users(allow_roles=['admin'])
def Student_Detail(request, pk):
  student = Student.objects.filter(pk=pk).first()
  return render(request, 'students/detail.html', {'student':student})
