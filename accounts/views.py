from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from users.decorators import unauthenticated_user

# Create your views here.

@unauthenticated_user
def login_view(request):
  if request.method == 'POST':
    username = request.POST.get('username')
    password = request.POST.get('password')
    
    user = authenticate(request, username=username, password=password)

    if user is not None:
      login(request, user)
      return redirect('dashboard')
    else:
      messages.info(request, 'Username OR Password is incorrect!')

  return render(request, 'accounts/login.html')

def logout_view(request):
  logout(request)
  return redirect('login')