from django.db import models
from users.models import Instructor

# Create your models here.
class Category(models.Model):
  name = models.CharField(max_length=100)

  def __str__(self):
    return self.name
  
class Tag(models.Model):
  name = models.CharField(max_length=(100))

  def __str__(self):
    return self.name
  
class Course(models.Model):
  name = models.CharField(max_length=100)
  category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
  instructor = models.ForeignKey(Instructor, on_delete=models.SET_NULL, null=True, related_name='courses')
  price = models.DecimalField(max_digits=10, decimal_places=2)
  description = models.TextField()
  image = models.ImageField(blank=True, null=True, upload_to='images')
  published_date = models.DateField(auto_now_add=True)

  def save(self, *args, **kwargs):
    # delete old img from folder, if new one is added when update
    try:
      old = Course.objects.get(pk=self.pk)
      
      if old.image and old.image != self.image:
          old.image.delete(save=False)
          
    except Course.DoesNotExist:
      pass  # Object is new, no old image to delete

    super().save(*args, **kwargs)

  def delete(self, *args, **kwargs):
    if self.image:
      # delete img from folder, when delete obj
      self.image.delete(save=False)

    super().delete(*args, **kwargs)

  def __str__(self):
    return self.name
  
class Lesson(models.Model):
  order = models.IntegerField()
  name = models.CharField(max_length=150)
  course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
  video_url = models.URLField(blank=True, null=True)
  duration = models.DurationField()
  resource_file = models.FileField(upload_to='files', blank=True, null=True)

  class Meta:
    unique_together = ('order', 'course')

  def __str__(self):
    return self.name

class CourseTag(models.Model):
  course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='tags')
  tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='courses')

  def __str__(self):
    return f"{self.course.name} - {self.tag.name}"
  