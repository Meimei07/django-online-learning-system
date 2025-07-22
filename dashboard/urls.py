from django.urls import path
from . import views

urlpatterns = [
  path('', views.dashboard_view, name='dashboard'),
  path('instructor-dashboard/', views.instructor_dashboard_view, name='instructor_dashboard'),
  path('student-dashboard/', views.student_dashboard_view, name='student_dashboard'),
]
