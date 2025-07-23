from django.db import models
from courses.models import Course
from users.models import Student

# Create your models here.
class Review(models.Model):
  STAR_CHOICES = {
    '5': '5',
    '4': '4',
    '3': '3',
    '2': '2',
    '1': '1',
  }

  student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True)
  course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, related_name='reviews')
  star = models.CharField(max_length=10, choices=STAR_CHOICES, default='5')
  comment = models.TextField()

  class Meta:
    unique_together = ('student', 'course')

  def __str__(self):
    return f"review - {self.student.name} x {self.course.name}"
