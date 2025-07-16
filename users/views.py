from django.shortcuts import render, redirect
from .models import Employee, Instructor, Student
from .forms import EmployeeForm, InstructorForm, StudentForm

# Create your views here.

#Employee
def List(request):
  employees = Employee.objects.all()
  return render(request, 'employees/list.html', {'employees':employees})

def Create(request):
  form = EmployeeForm(request.POST or None)

  if form.is_valid():
    form.save()
    return redirect('users:employee_list')
  
  return render(request, 'employees/create_update.html', {'form':form})

def Update(request, pk):
  employee = Employee.objects.filter(pk=pk).first()
  form = EmployeeForm(request.POST or None, instance=employee)

  if form.is_valid():
    form.save()
    return redirect('users:employee_list')

  return render(request, 'employees/create_update.html', {'form':form})

def Delete(request, pk):
  employee = Employee.objects.filter(pk=pk).first()

  if request.method == 'POST':
    employee.delete()
    return redirect('users:employee_list')
  
  return render(request, 'employees/delete.html', {'employee':employee})

#Instructor
def Instructor_List(request):
  instructors = Instructor.objects.all()
  return render(request, 'instructors/list.html', {'instructors':instructors})

def Instructor_Create(request):
  form = InstructorForm(request.POST or None)

  if form.is_valid():
    form.save()
    return redirect('users:instructor_list')
  
  return render(request, 'instructors/create_update.html', {'form':form})

def Instructor_Update(request, pk):
  instructor = Instructor.objects.filter(pk=pk).first()
  form = InstructorForm(request.POST or None, instance=instructor)

  if form.is_valid():
    form.save()
    return redirect('users:instructor_list')

  return render(request, 'instructors/create_update.html', {'form':form})

def Instructor_Delete(request, pk):
  instructor = Instructor.objects.filter(pk=pk).first()

  if request.method == 'POST':
    instructor.delete()
    return redirect('users:instructor_list')
  
  return render(request, 'instructors/delete.html', {'instructor':instructor})

#Student
def Student_List(request):
  students = Student.objects.all()
  return render(request, 'students/list.html', {'students':students})

def Student_Create(request):
  form = StudentForm(request.POST or None)

  if form.is_valid():
    form.save()
    return redirect('users:student_list')
  
  return render(request, 'students/create_update.html', {'form':form})

def Student_Update(request, pk):
  student = Student.objects.filter(pk=pk).first()
  form = StudentForm(request.POST or None, instance=student)

  if form.is_valid():
    form.save()
    return redirect('users:student_list')

  return render(request, 'students/create_update.html', {'form':form})

def Student_Delete(request, pk):
  student = Student.objects.filter(pk=pk).first()

  if request.method == 'POST':
    student.delete()
    return redirect('users:student_list')
  
  return render(request, 'students/delete.html', {'student':student})
