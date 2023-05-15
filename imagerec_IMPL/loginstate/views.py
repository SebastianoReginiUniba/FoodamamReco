from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# API
from py_edamam import Edamam
import json

from .forms import *

# Neural network model
import tensorflow as tf
from PIL import Image
import numpy as np

# Chatbot
#from django.http import JsonResponse
#from .food_chatbot import chatbot


from tensorflow.keras.models import load_model

MODEL_PATH = "food_classifier.h5"
model = load_model(MODEL_PATH, compile=False)

def predict(image_path):
    preprocessed_image = preprocess_image(image_path)
    prediction = model.predict(preprocessed_image)
    # Process the prediction to get the recognized class

    return recognized_class

input_dimension = 224
def preprocess_image(image_file):
    img = Image.open(image_file)
    img = img.resize((input_dimension, input_dimension))  # Replace input_width and input_height with your model's input dimensions
    img_array = np.array(img) / 255.0  # Normalize pixel values
    img_array = np.expand_dims(img_array, axis=0)  # Add a batch dimension
    return img_array

def show_recipe_options(request, resultRecipe):
    recipeInput = resultRecipe

    e = Edamam(recipes_appid='d0eeda40',
            recipes_appkey='30d3b1b95a3b059152766628369771f7')

    a = e.search_recipe(recipeInput)
    hits = a["hits"]
    
    print(recipeInput)
    print(hits)

    if request.method == 'POST' and 'hit_choice' in request.POST:
        count = int(request.POST['hit_choice'])
        print("\n\n")
        print('Grassi: ' + str(a['hits'][count]['recipe']['digest'][0]['total']) + " " + str(a['hits'][count]['recipe']['digest'][0]['unit']))
        print('Carboidrati: ' + str(a['hits'][count]['recipe']['digest'][1]['total']) + " " + str(a['hits'][count]['recipe']['digest'][1]['unit']))
        print('Proteine: ' + str(a['hits'][count]['recipe']['digest'][2]['total']) + " " + str(a['hits'][count]['recipe']['digest'][2]['unit']))
    return hits


# Create your views here.

@login_required(login_url='login')
def home(request):
    form = ImageForm(request.POST)
    img = ImageUpload.objects.last()
    resultRecipe = ""
    with open('classes.txt', 'r') as f:
        classes = [line.strip() for line in f.readlines()]

    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            img = ImageUpload.objects.last()
            preprocessed_image = preprocess_image(img.picture.path)
            prediction = np.argmax(model.predict(preprocessed_image))
            resultRecipe = classes[prediction]
            resultRecipe = resultRecipe.replace('_', ' ')

            show_recipe_options(request, resultRecipe)
        else:
            form = ImageForm()

        img = ImageUpload.objects.last()

		# ----

        
    context = {'img': img, 'form': form}#, 'hits': hits}, 'recognized_class': recognized_class}
    return render(request, 'loginstate/home.html', context)

@login_required(login_url='login')
def chatbot(request):
	'''
	user_input = request.GET.get('msg')
	response = chatbot.get_response(user_input)
	print(JsonResponse({'response': str(response)}))
	#context = {'form': form}
	'''

	return render(request, 'loginstate/chatbot.html')#, context)

# -----------------------------------------------------------------------

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