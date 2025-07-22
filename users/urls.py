from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
  #login
  path('login/', views.login_view, name='login'),
  path('logout/', views.logout_view, name='logout'),

  #employees
  path('employees/', views.List, name='employee_list'),
  path('employees/create/', views.Create, name='employee_create'),
  path('employees/update/<int:pk>/', views.Update, name='employee_update'),
  path('employees/delete/<int:pk>/', views.Delete, name='employee_delete'),

  #instructors
  path('instructors/', views.Instructor_List, name='instructor_list'),
  path('instructors/create/', views.Instructor_Create, name='instructor_create'),
  path('instructors/update/<int:pk>/', views.Instructor_Update, name='instructor_update'),
  path('instructors/delete/<int:pk>/', views.Instructor_Delete, name='instructor_delete'),
  path('instructors/detail/<int:pk>/', views.Instructor_Detail, name='instructor_detail'),

  #students
  path('students/', views.Student_List, name='student_list'),
  path('students/create/', views.Student_Create, name='student_create'),
  path('students/update/<int:pk>/', views.Student_Update, name='student_update'),
  path('students/delete/<int:pk>/', views.Student_Delete, name='student_delete'),
  path('students/detail/<int:pk>/', views.Student_Detail, name='student_detail'),
]
