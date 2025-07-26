from django.contrib import admin
from .models import Category, Tag, Course, Lesson, CourseTag

# Register your models here.
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(CourseTag)
