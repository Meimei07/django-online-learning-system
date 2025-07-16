from django.contrib import admin
from .models import Employee, Instructor, Student

# Register your models here.
admin.site.register(Employee)
admin.site.register(Instructor)
admin.site.register(Student)
