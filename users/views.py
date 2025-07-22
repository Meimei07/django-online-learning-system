from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Employee, Instructor, Student
from .forms import EmployeeForm, InstructorForm, StudentForm, CustomUserForm
from .decorators import unauthenticated_user, allow_users

# Create your views here.

# Login

@unauthenticated_user
def login_view(request):
  if request.method == 'POST':
    username = request.POST.get('username')
    password = request.POST.get('password')
    
    user = authenticate(request, username=username, password=password)

    if user is not None:
      login(request, user)
      return redirect('dashboard')
    else:
      messages.info(request, 'Username OR Password is incorrect!')

  return render(request, 'users/login.html')

def logout_view(request):
  logout(request)
  return redirect('users:login')

#Employee

@login_required(login_url='users:login')
@allow_users(allow_roles=['admin'])
def List(request):
  employees = Employee.objects.all()
  return render(request, 'employees/list.html', {'employees':employees})

@login_required(login_url='users:login')
@allow_users(allow_roles=['admin'])
def Create(request):
  form = EmployeeForm(request.POST or None)

  if form.is_valid():
    form.save()
    return redirect('users:employee_list')
  
  return render(request, 'employees/create_update.html', {'form':form})

@login_required(login_url='users:login')
@allow_users(allow_roles=['admin'])
def Update(request, pk):
  employee = Employee.objects.filter(pk=pk).first()
  form = EmployeeForm(request.POST or None, instance=employee)

  if form.is_valid():
    form.save()
    return redirect('users:employee_list')

  return render(request, 'employees/create_update.html', {'form':form})

@login_required(login_url='users:login')
@allow_users(allow_roles=['admin'])
def Delete(request, pk):
  employee = Employee.objects.filter(pk=pk).first()

  if request.method == 'POST':
    employee.delete()
    return redirect('users:employee_list')
  
  return render(request, 'employees/delete.html', {'employee':employee})

#Instructor

@login_required(login_url='users:login')
@allow_users(allow_roles=['admin'])
def Instructor_List(request):
  instructors = Instructor.objects.all()
  return render(request, 'instructors/list.html', {'instructors':instructors})

@login_required(login_url='users:login')
@allow_users(allow_roles=['admin'])
def Instructor_Create(request):
  form = InstructorForm(request.POST or None)

  if form.is_valid():
    form.save()
    return redirect('users:instructor_list')
  
  return render(request, 'instructors/create_update.html', {'form':form})

@login_required(login_url='users:login')
@allow_users(allow_roles=['admin'])
def Instructor_Update(request, pk):
  instructor = Instructor.objects.filter(pk=pk).first()
  form = InstructorForm(request.POST or None, instance=instructor)

  if form.is_valid():
    form.save()
    return redirect('users:instructor_list')

  return render(request, 'instructors/create_update.html', {'form':form})

@login_required(login_url='users:login')
@allow_users(allow_roles=['admin'])
def Instructor_Delete(request, pk):
  instructor = Instructor.objects.filter(pk=pk).first()

  if request.method == 'POST':
    instructor.delete()
    return redirect('users:instructor_list')
  
  return render(request, 'instructors/delete.html', {'instructor':instructor})

@login_required(login_url='users:login')
@allow_users(allow_roles=['admin'])
def Instructor_Detail(request, pk):
  instructor = Instructor.objects.filter(pk=pk).first()
  return render(request, 'instructors/detail.html', {'instructor':instructor})

#Student

@login_required(login_url='users:login')
@allow_users(allow_roles=['admin'])
def Student_List(request):
  students = Student.objects.all()
  return render(request, 'students/list.html', {'students':students})

@login_required(login_url='users:login')
@allow_users(allow_roles=['admin'])
def Student_Create(request):
  form = StudentForm(request.POST or None)

  if form.is_valid():
    form.save()
    return redirect('users:student_list')
  
  return render(request, 'students/create_update.html', {'form':form})

@login_required(login_url='users:login')
@allow_users(allow_roles=['admin'])
def Student_Update(request, pk):
  student = Student.objects.filter(pk=pk).first()
  form = StudentForm(request.POST or None, instance=student)

  if form.is_valid():
    form.save()
    return redirect('users:student_list')

  return render(request, 'students/create_update.html', {'form':form})

@login_required(login_url='users:login')
@allow_users(allow_roles=['admin'])
def Student_Delete(request, pk):
  student = Student.objects.filter(pk=pk).first()

  if request.method == 'POST':
    student.delete()
    return redirect('users:student_list')
  
  return render(request, 'students/delete.html', {'student':student})

@login_required(login_url='users:login')
@allow_users(allow_roles=['admin'])
def Student_Detail(request, pk):
  student = Student.objects.filter(pk=pk).first()
  return render(request, 'students/detail.html', {'student':student})
