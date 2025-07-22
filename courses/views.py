from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

from .models import Category, Tag, Course, Lesson, CourseTag
from .forms import CategoryForm, TagForm ,CourseForm, CourseFormByInstructor, LessonForm, CourseTagForm
from users.models import Instructor
from users.decorators import allow_users

# Create your views here.

#Category

@login_required(login_url='users:login')
@allow_users(allow_roles=['admin', 'instructor'])
def Category_List(request):
  categories = Category.objects.all()
  tags = Tag.objects.all()
  return render(request, 'categories/list.html', {'categories':categories, 'tags':tags})

@login_required(login_url='users:login')
@allow_users(allow_roles=['admin', 'instructor'])
def Category_Create(request):
  form = CategoryForm(request.POST or None)

  if form.is_valid():
    form.save()
    return redirect('courses:category_list')
  
  return render(request, 'categories/create_update.html', {'form':form})

@login_required(login_url='users:login')
@allow_users(allow_roles=['admin', 'instructor'])
def Category_Update(request, pk):
  category = Category.objects.filter(pk=pk).first()
  form = CategoryForm(request.POST or None, instance=category)

  if form.is_valid():
    form.save()
    return redirect('courses:category_list')

  return render(request, 'categories/create_update.html', {'form':form})

@login_required(login_url='users:login')
@allow_users(allow_roles=['admin', 'instructor'])
def Category_Delete(request, pk):
  category = Category.objects.filter(pk=pk).first()

  if request.method == 'POST':
    category.delete()
    return redirect('courses:category_list')
  
  return render(request, 'categories/delete.html', {'category':category})

#Course
@login_required(login_url='users:login')
@allow_users(allow_roles=['admin', 'instructor', 'student'])
def Course_List(request):  
  login_user = request.user.groups.first().name

  if login_user == 'instructor':
    # filter to get that instructor's courses only
    instructor = get_object_or_404(Instructor, name=request.user)
    courses = instructor.courses.all() 
  else:
    courses = Course.objects.all()

  categories = Category.objects.all()
  tags = Tag.objects.all()
  instructors = Instructor.objects.all()

  selected_category_id = request.GET.get('category')
  if selected_category_id:
    courses = courses.filter(category_id=selected_category_id)
  
  selected_tags = request.GET.getlist('tag')
  if selected_tags:
    for selected_tag in selected_tags:
      courses = courses.filter(tags__tag_id=selected_tag)

  selected_instructor_id = request.GET.get('instructor')
  if selected_instructor_id:
    courses = courses.filter(instructor_id=selected_instructor_id)

  context = {
    'courses': courses,
    'categories': categories,
    'tags': tags,
    'instructors': instructors,
    'selected_category_id': int(selected_category_id) if selected_category_id else None,
    'selected_tags': [int(t) for t in selected_tags],
    'selected_instructor_id': int(selected_instructor_id) if selected_instructor_id else None,
  }

  return render(request, 'courses/list.html', context)

@login_required(login_url='users:login')
@allow_users(allow_roles=['admin', 'instructor'])
def Course_Create(request):
  login_user = request.user.groups.first().name

  if login_user == 'instructor':
    login_id = request.user.instructor.id
    instructor = Instructor.objects.get(pk=login_id)

    form = CourseFormByInstructor(initial={'instructor':instructor})

    if request.method == 'POST':
      form = CourseFormByInstructor(request.POST or None, request.FILES)

      if form.is_valid():
        course = form.save(commit=False)
        course.instructor = instructor
        course.save()
        return redirect('courses:course_list')
      
    else: form = CourseFormByInstructor()

  elif login_user == 'admin':
    if request.method == 'POST':
      form = CourseForm(request.POST or None, request.FILES)

      if form.is_valid():
        form.save()
        return redirect('courses:course_list')   
      
    else:
      form = CourseForm()
    
  return render(request, 'courses/create_update.html', {'form':form})

@login_required(login_url='users:login')
@allow_users(allow_roles=['admin', 'instructor'])
def Course_Update(request, pk):
  course = Course.objects.filter(pk=pk).first()
  login_user = request.user.groups.first().name

  if login_user == 'instructor':
    login_id = request.user.instructor.id
    instructor = Instructor.objects.get(pk=login_id)

    form = CourseFormByInstructor(initial={'instructor':instructor})

    if request.method == 'POST':
      form = CourseFormByInstructor(request.POST or None, request.FILES, instance=course)

      if form.is_valid():
        course = form.save(commit=False)
        course.instructor = instructor
        course.save()
        return redirect('courses:course_detail', pk=course.id)
      
    else:
      form = CourseFormByInstructor(instance=course)

  elif login_user == 'admin':
    if request.method == 'POST':
      form = CourseForm(request.POST or None,  request.FILES, instance=course)

      if form.is_valid():
        form.save()
        return redirect('courses:course_detail', pk=course.id)
    else:
      form = CourseForm(instance=course)

  return render(request, 'courses/create_update.html', {'form':form, 'course':course})

@login_required(login_url='users:login')
@allow_users(allow_roles=['admin', 'instructor'])
def Course_Delete(request, pk):
  course = Course.objects.filter(pk=pk).first()

  if request.method == 'POST':
    course.delete()
    return redirect('courses:course_list')
  
  return render(request, 'courses/delete.html', {'course':course})

@login_required(login_url='users:login')
@allow_users(allow_roles=['admin', 'instructor', 'student'])
def Course_Detail(request, pk):
  course = Course.objects.filter(pk=pk).first()
  form = CourseTagForm(initial={'course':course})
  order_lessons = course.lessons.all().order_by('order')

  total_duration = course.lessons.aggregate(total=Sum('duration'))['total'] 
  total_lessons = course.lessons.count()

  # add tag to course
  if request.method == 'POST' and 'add-tag' in request.POST:
    form = CourseTagForm(request.POST or None)
    
    if form.is_valid():
      course_tag = form.save(commit=False)
      course_tag.course = course
      course_tag.save()
      return redirect('courses:course_detail', pk=course.id)

  context = {
    'course':course, 
    'lessons': order_lessons,
    'form':form, 
    'total_duration':total_duration,
    'total_lessons': total_lessons,
  }

  return render(request, 'courses/detail.html', context)

#Tag

@login_required(login_url='users:login')
@allow_users(allow_roles=['admin', 'instructor'])
def Tag_Create(request):
  form = TagForm(request.POST or None)

  if form.is_valid():
    form.save()
    return redirect('courses:category_list')
  
  return render(request, 'tags/create_update.html', {'form':form})

@login_required(login_url='users:login')
@allow_users(allow_roles=['admin', 'instructor'])
def Tag_Update(request, pk):
  tag = Tag.objects.filter(pk=pk).first()
  form = TagForm(request.POST or None, instance=tag)

  if form.is_valid():
    form.save()
    return redirect('courses:category_list')

  return render(request, 'tags/create_update.html', {'form':form})

@login_required(login_url='users:login')
@allow_users(allow_roles=['admin', 'instructor'])
def Tag_Delete(request, pk):
  tag = Tag.objects.filter(pk=pk).first()

  if request.method == 'POST':
    tag.delete()
    return redirect('courses:category_list')
  
  return render(request, 'tags/delete.html', {'tag':tag})

#Lesson

@login_required(login_url='users:login')
@allow_users(allow_roles=['admin', 'instructor'])
def Lesson_Create(request, pk): # pk of course
  course = Course.objects.filter(pk=pk).first()
  form = LessonForm(initial={'course':course})

  if request.method == 'POST':
    form = LessonForm(request.POST or None, request.FILES)
    order = int(request.POST.get('order'))

    if form.is_valid():
      if Lesson.objects.filter(course=course, order=order).exists():
        messages.error(request, f"Order {order} already exists in this course.")
        return render(request, 'lessons/create_update.html', {'form':form, 'course': course})
      
      lesson = form.save(commit=False)
      lesson.course = course
      lesson.save()
      return redirect('courses:course_detail', pk=course.id)   
  else:
    form = LessonForm()
    
  return render(request, 'lessons/create_update.html', {'form':form, 'course':course})

@login_required(login_url='users:login')
@allow_users(allow_roles=['admin', 'instructor'])
def Lesson_Update(request, pk):
  lesson = Lesson.objects.filter(pk=pk).first()
  
  if request.method == 'POST':
    form = LessonForm(request.POST or None, request.FILES, instance=lesson)

    if form.is_valid():
      form.save()
      return redirect('courses:course_detail', pk=lesson.course.id)
  else:
    form = LessonForm(instance=lesson)
    
  return render(request, 'lessons/create_update.html', {'form':form, 'course':lesson.course})

@login_required(login_url='users:login')
@allow_users(allow_roles=['admin', 'instructor'])
def Lesson_Delete(request, pk):
  lesson = Lesson.objects.filter(pk=pk).first()

  if request.method == 'POST':
    lesson.delete()
    return redirect('courses:course_detail', pk=lesson.course.id)
    
  return render(request, 'lessons/delete.html', {'lesson':lesson})

#CourseTag

@login_required(login_url='users:login')
@allow_users(allow_roles=['admin', 'instructor'])
def Course_Tag_Delete(request, pk) :
  course_tag = CourseTag.objects.filter(pk=pk).first()

  if request.method == 'POST':
    course_tag.delete()

  return redirect('courses:course_detail', pk=course_tag.course.id)
