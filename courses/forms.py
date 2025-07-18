from django import forms
from .models import Category, Tag, Course, Lesson, CourseTag

class CategoryForm(forms.ModelForm):
  class Meta:
    model = Category
    fields = '__all__'

class TagForm(forms.ModelForm):
  class Meta:
    model = Tag
    fields = '__all__'

class CourseForm(forms.ModelForm):
  class Meta:
    model = Course
    fields = '__all__'

    widgets = {
      'image': forms.FileInput(),
      'published_date': forms.DateInput(attrs={'readonly':'readonly'}),
    }

class LessonForm(forms.ModelForm):
  class Meta:
    model = Lesson
    fields = ['order', 'name', 'video_url', 'duration', 'resource_file']

    widgets = {
      'resource_file': forms.FileInput(),
    }

class CourseTagForm(forms.ModelForm):
  class Meta:
    model = CourseTag
    fields = ['tag']
