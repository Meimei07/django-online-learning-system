from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Employee, Instructor, Student

class CustomUserForm(UserCreationForm):
  class Meta:
    model = User
    fields = ['username', 'password1']

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    # Remove password2 field
    self.fields.pop('password2', None)
    self.fields['password1'].widget = forms.TextInput(attrs={'type':'text'})

class EmployeeForm(forms.ModelForm):
  class Meta:
    model = Employee
    fields = ['name', 'age', 'email', 'phone', 'address']

class InstructorForm(forms.ModelForm):
  class Meta:
    model = Instructor
    fields = ['name', 'age', 'email', 'phone', 'address', 'salary']

class StudentForm(forms.ModelForm):
  class Meta:
    model = Student
    fields = ['name', 'age', 'gender', 'email', 'phone', 'address']
