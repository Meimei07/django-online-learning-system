from django.shortcuts import render, redirect
from .models import Category, Tag, Course, Lesson, CourseTag
from .forms import CategoryForm, TagForm ,CourseForm, LessonForm, CourseTagForm
from users.models import Instructor

# Create your views here.

#Category
def Category_List(request):
  categories = Category.objects.all()
  tags = Tag.objects.all()
  return render(request, 'categories/list.html', {'categories':categories, 'tags':tags})

def Category_Create(request):
  form = CategoryForm(request.POST or None)

  if form.is_valid():
    form.save()
    return redirect('courses:category_list')
  
  return render(request, 'categories/create_update.html', {'form':form})

def Category_Update(request, pk):
  category = Category.objects.filter(pk=pk).first()
  form = CategoryForm(request.POST or None, instance=category)

  if form.is_valid():
    form.save()
    return redirect('courses:category_list')

  return render(request, 'categories/create_update.html', {'form':form})

def Category_Delete(request, pk):
  category = Category.objects.filter(pk=pk).first()

  if request.method == 'POST':
    category.delete()
    return redirect('courses:category_list')
  
  return render(request, 'categories/delete.html', {'category':category})

#Course
def Course_List(request):  
  courses = Course.objects.all()
  categories = Category.objects.all()
  tags = Tag.objects.all()
  instructors = Instructor.objects.all()

  selected_category_id = request.GET.get('category')
  if selected_category_id:
    courses = courses.filter(category_id=selected_category_id)
  else:
    request.session.flush()

  selected_instructor_id = request.GET.get('instructor')
  if selected_instructor_id:
    courses = courses.filter(instructor_id=selected_instructor_id)

  selected_tags = request.session.get('selected_tags', [])
  selected_tag_id = request.GET.get('tag')

  if not selected_tag_id:
    # request.session.flush()
    print('no tag')
    request.session.flush()
    print(selected_tags)

    context = {
      'courses': courses,
      'categories': categories,
      'tags': tags,
      'instructors': instructors,
      'selected_category_id': int(selected_category_id) if selected_category_id else None,
      'selected_instructor_id': int(selected_instructor_id) if selected_instructor_id else None,
    }

    return render(request, 'courses/list.html', context)

  if selected_tag_id in selected_tags:
    print('remove')
    selected_tags.remove(selected_tag_id)
  else:
    print(request.GET.get('tag'))
    selected_tags.append(selected_tag_id)

  request.session['selected_tags'] = selected_tags
  print(selected_tags)

  for selected_tag in selected_tags:
    courses = courses.filter(tags__tag_id=selected_tag)

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

def Course_Create(request):
  if request.method == 'POST':
    form = CourseForm(request.POST or None, request.FILES)

    if form.is_valid():
      form.save()
      return redirect('courses:course_list')   
  else:
    form = CourseForm()
    
  return render(request, 'courses/create_update.html', {'form':form})

def Course_Update(request, pk):
  course = Course.objects.filter(pk=pk).first()

  if request.method == 'POST':
    form = CourseForm(request.POST or None,  request.FILES, instance=course)

    if form.is_valid():
      form.save()
      return redirect('courses:course_detail', pk=course.id)
  else:
    form = CourseForm(instance=course)

  return render(request, 'courses/create_update.html', {'form':form, 'course':course})

def Course_Delete(request, pk):
  course = Course.objects.filter(pk=pk).first()

  if request.method == 'POST':
    course.delete()
    return redirect('courses:course_list')
  
  return render(request, 'courses/delete.html', {'course':course})

def Course_Detail(request, pk):
  course = Course.objects.filter(pk=pk).first()
  form = CourseTagForm(initial={'course':course})

  # add tag to course
  if request.method == 'POST' and 'add-tag' in request.POST:
    form = CourseTagForm(request.POST or None)
    
    if form.is_valid():
      course_tag = form.save(commit=False)
      course_tag.course = course
      course_tag.save()
      return redirect('courses:course_detail', pk=course.id)

  return render(request, 'courses/detail.html', {'course':course, 'form':form})

#Tag
def Tag_Create(request):
  form = TagForm(request.POST or None)

  if form.is_valid():
    form.save()
    return redirect('courses:category_list')
  
  return render(request, 'tags/create_update.html', {'form':form})

def Tag_Update(request, pk):
  tag = Tag.objects.filter(pk=pk).first()
  form = TagForm(request.POST or None, instance=tag)

  if form.is_valid():
    form.save()
    return redirect('courses:category_list')

  return render(request, 'tags/create_update.html', {'form':form})

def Tag_Delete(request, pk):
  tag = Tag.objects.filter(pk=pk).first()

  if request.method == 'POST':
    tag.delete()
    return redirect('courses:category_list')
  
  return render(request, 'tags/delete.html', {'tag':tag})

#Lesson
def Lesson_Create(request, pk): # pk of course
  course = Course.objects.filter(pk=pk).first()
  form = LessonForm(initial={'course':course})

  if request.method == 'POST':
    form = LessonForm(request.POST or None, request.FILES)

    if form.is_valid():
      lesson = form.save(commit=False)
      lesson.course = course
      lesson.save()
      return redirect('courses:course_detail', pk=course.id)   
  else:
    form = LessonForm()
    
  return render(request, 'lessons/create_update.html', {'form':form, 'course':course})

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

def Lesson_Delete(request, pk):
  lesson = Lesson.objects.filter(pk=pk).first()

  if request.method == 'POST':
    lesson.delete()
    return redirect('courses:course_detail', pk=lesson.course.id)
    
  return render(request, 'lessons/delete.html', {'lesson':lesson})

#CourseTag
def Course_Tag_Delete(request, pk) :
  course_tag = CourseTag.objects.filter(pk=pk).first()

  if request.method == 'POST':
    course_tag.delete()

  return redirect('courses:course_detail', pk=course_tag.course.id)
