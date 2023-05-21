from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *
from django.forms import ModelForm

class CreateUserForm(UserCreationForm):
	class Meta:
		model = CustomUser
		fields = ['username', 'email', 'password1', 'password2', 'allergies', 'diets']

class ImageForm(ModelForm):
	class Meta:
		model = ImageUpload
		fields = '__all__'