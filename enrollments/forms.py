from django import forms
from .models import Enrollment

class AddEnrollmentForm(forms.ModelForm):
  class Meta:
    model = Enrollment
    fields = ['student', 'course']

class UpdateEnrollmentForm(forms.ModelForm):
  class Meta:
    model = Enrollment
    fields = '__all__'

class EnrollmentFormInCourse(forms.ModelForm):
  class Meta:
    model = Enrollment
    fields = ['student']

    widgets = {
      'enrolled_date': forms.DateInput(attrs={'readonly':'readonly'}),
      'status': forms.TextInput(attrs={'readonly':'readonly'}),
    }

class EnrollmentFormByStudent(forms.ModelForm):
  class Meta:
    model = Enrollment
    fields = []

    widgets = {
      'enrolled_date': forms.DateInput(attrs={'readonly':'readonly'}),
      'status': forms.TextInput(attrs={'readonly':'readonly'}),
    }
