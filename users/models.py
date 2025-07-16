from django.db import models

# Create your models here.
class Employee(models.Model):
  name = models.CharField(max_length=100)
  age = models.IntegerField()
  email = models.EmailField()
  phone = models.CharField(max_length=20)
  address = models.CharField(max_length=150)

  def __str__(self):
    return self.name

class Instructor(models.Model):
  name = models.CharField(max_length=100)
  age = models.IntegerField()
  email = models.EmailField()
  phone = models.CharField(max_length=20)
  address = models.CharField(max_length=150)
  salary = models.DecimalField(max_digits=10, decimal_places=2)

  def __str__(self):
    return self.name

class Student(models.Model):
  GENDER_CHOICES = {
    'Female': 'Female',
    'Male': 'Male'
  }

  name = models.CharField(max_length=100)
  age = models.IntegerField()
  gender = models.CharField(max_length=15, choices=GENDER_CHOICES)
  email = models.EmailField()
  phone = models.CharField(max_length=20)
  address = models.CharField(max_length=150)

  def __str__(self):
    return self.name
  