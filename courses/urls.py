from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
  #categories
  path('categories/', views.Category_List, name='category_list'),
  path('categories/create/', views.Category_Create, name='category_create'),
  path('categories/update/<int:pk>/', views.Category_Update, name='category_update'),
  path('categories/delete/<int:pk>/', views.Category_Delete, name='category_delete'),

  #tags
  path('tags/create/', views.Tag_Create, name='tag_create'),
  path('tags/update/<int:pk>/', views.Tag_Update, name='tag_update'),
  path('tags/delete/<int:pk>/', views.Tag_Delete, name='tag_delete'),
  
  #courses
  path('courses/', views.Course_List, name='course_list'),
  path('courses/create/', views.Course_Create, name='course_create'),
  path('courses/update/<int:pk>/', views.Course_Update, name='course_update'),
  path('courses/delete/<int:pk>/', views.Course_Delete, name='course_delete'),
  path('courses/detail/<int:pk>/', views.Course_Detail, name='course_detail'),

  #lessons
  path('lessons/create/<int:pk>', views.Lesson_Create, name='lesson_create'),
  path('lessons/update/<int:pk>/', views.Lesson_Update, name='lesson_update'),
  path('lessons/delete/<int:pk>/', views.Lesson_Delete, name='lesson_delete'),

  #course_tags
  path('course_tag/delete/<int:pk>/', views.Course_Tag_Delete, name='course_tag_delete'),
   
]

