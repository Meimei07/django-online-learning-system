from django.http import HttpResponse
from django.shortcuts import redirect

# if put this decorator above login_view, it means
# it'll check the condition below first
# if user is already authenticated, send them to dashboard
# else will run the login_view
def unauthenticated_user(view_func):
  def wrapper_func(request, *args, **kwargs):
    if request.user.is_authenticated:
      return redirect('dashboard')
    else:
      return view_func(request, *args, **kwargs)
  
  return wrapper_func

def allow_users(allow_roles=[]):
  def decorator(view_func):
    def wrapper_func(request, *args, **kwargs):

      group = None
      if request.user.groups.exists():
        group = request.user.groups.all()[0].name
        print('login group: ', group)

      print('allow group: ', allow_roles)

      if group in allow_roles:
        return view_func(request, *args, **kwargs)
      else:
        return HttpResponse('You are not authorize to view this page!')

    return wrapper_func
  return decorator

def admin_only(view_func):
  def wrapper_func(request, *args, **kwargs):
    group = None
    if request.user.groups.exists():
      group = request.user.groups.all()[0].name

    if group == 'instructor':
      return redirect('instructor_dashboard')
    elif group == 'student': 
      return redirect('student_dashboard')

    return view_func(request, *args, **kwargs)
  
  return wrapper_func
