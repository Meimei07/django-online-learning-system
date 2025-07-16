from django import forms
from .models import Employee, Instructor, Student

class EmployeeForm(forms.ModelForm):
  class Meta:
    model = Employee
    fields = '__all__'

class InstructorForm(forms.ModelForm):
  class Meta:
    model = Instructor
    fields = '__all__'

class StudentForm(forms.ModelForm):
  class Meta:
    model = Student
    fields = '__all__'
