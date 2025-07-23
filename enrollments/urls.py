from django.urls import path
from . import views

app_name = 'enrollments'

urlpatterns = [
  path('', views.enrollment_list, name='enrollment_list'),
  path('create/', views.enrollment_create, name='enrollment_create'),
  path('update/<int:pk>/', views.enrollment_update, name='enrollment_update'),
  path('delete/<int:pk>/', views.enrollment_delete, name='enrollment_delete'),

  path('create/<int:pk>/', views.enrollment_create_in_course, name='enrollment_create_in_course'),
]
