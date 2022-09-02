from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import *

# Create your views here.

@login_required(login_url='login')
def home(request):
	form = ImageForm(request.POST)

	if request.method == 'POST':
		form = ImageForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
		else:
			form=ImageForm()

	img = ImageUpload.objects.last()
	context = {'img':img,'form':form}
	return render(request, 'loginstate/home.html', context)

# Registration ----------------------------------------------------------

def registrationPage(request):
	form = CreateUserForm()

	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			form.save()
			user = form.cleaned_data.get('username') # Recupero username appena inserito
			messages.success(request, 'Account created for ' + user)
			return redirect('login')

	context = {'form':form}
	return render(request, 'loginstate/registration.html', context)

# -----------------------------------------------------------------------

# Login -----------------------------------------------------------------

def loginPage(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('home')
		else:
			messages.info(request,'Wrong username or password')

	context = {}
	return render(request, 'loginstate/login.html', context)

# -----------------------------------------------------------------------

# Logout ----------------------------------------------------------------

def logoutUser(request):
	logout(request)
	return redirect('login')

# -----------------------------------------------------------------------