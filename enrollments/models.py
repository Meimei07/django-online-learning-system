from django.db import models
from users.models import Student
from courses.models import Course

# Create your models here.
class Enrollment(models.Model):
  student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True, related_name='enrollments')
  course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, related_name='enrollments')
  enrolled_date = models.DateField(auto_now_add=True)

  class Meta:
    unique_together = ('student', 'course')

  def __str__(self):
    return f"{self.student.name} - {self.course.name}"
  