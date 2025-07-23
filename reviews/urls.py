from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
  path('', views.review_list, name='review_list'),
  path('create/<int:pk>/', views.review_create, name='review_create'),
]
