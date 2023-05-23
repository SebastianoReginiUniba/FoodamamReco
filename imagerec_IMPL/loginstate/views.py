from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import *
from .models import ALLERGIES_DICT, DIETS_DICT

# API
from py_edamam import Edamam
import json
import urllib.parse
from urllib.parse import quote
''''''
API_ID = 'd0eeda40'
API_KEY = '30d3b1b95a3b059152766628369771f7'

# Neural network model
import tensorflow as tf
from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np
''''''
MODEL_PATH = "food_classifier.h5"
model = load_model(MODEL_PATH, compile=False)
input_dimension = 224

# Recipe infos
import requests
from django.http import JsonResponse

# Chatbot
'''
from django.http import JsonResponse
from .food_chatbot import chatbot
'''

def registerPage(request):
    form = CreateUserForm()
    form.allergy_images = CustomUser.allergy_images
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)
            return redirect('login')

    context = {'form': form}
    return render(request, 'register.html', context)

def predict(image_path):
    with open('classes.txt', 'r') as f:
        classes = [line.strip() for line in f.readlines()]
    preprocessed_image = preprocess_image(image_path)
    prediction = model.predict(preprocessed_image)
    prediction = np.argmax(prediction)
    recognized_class = classes[prediction]
    recognized_class = recognized_class.replace('_', ' ')
    return recognized_class

def preprocess_image(image_file):
    img = Image.open(image_file)
    img = img.resize((input_dimension, input_dimension))
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

@login_required(login_url='login')
def recipeDetails(request):
    user_characteristics = []
    user = request.user
    uri = request.GET.get('uri')
    label = request.GET.get('label')

    for allergy in user.allergies:
        user_characteristics.append(ALLERGIES_DICT[allergy])
        user_characteristics.append(ALLERGIES_DICT[allergy]+"-Free")
    for diets in user.diets:
        user_characteristics.append(DIETS_DICT[diets])
        user_characteristics.append(DIETS_DICT[diets]+"-Free")
        
    
    e = Edamam(recipes_appid=API_ID,recipes_appkey=API_KEY)
    
    recipe_data = e.search_recipe(label)['hits']
    for hit in recipe_data:
        recipe = hit['recipe']
        if recipe['uri'] == uri and recipe['label'] == label:
            this_recipe = recipe
            break

    context = {'this_recipe': this_recipe, 'user_characteristics':user_characteristics}
    return render(request, 'loginstate/recipeDetails.html', context)

@login_required(login_url='login')
def home(request):
    form = ImageForm(request.POST)
    img = ImageUpload.objects.last()
    resultRecipe = ""
    hits = []
    recognized_class = ""

    # Check for forms that send "POST"
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            img = ImageUpload.objects.last()
            if img.picture:
                recognized_class = predict(img.picture.path)

                # Update the image object with the recognized recipe label
                img.recipe_label = recognized_class
                img.save()

                # Get recipe hits based on the recognized class
                e = Edamam(recipes_appid=API_ID,
                           recipes_appkey=API_KEY)
                response = e.search_recipe(recognized_class)
                hits = []
                hits = [{'recipe': {'uri': urllib.parse.quote(result['recipe']['uri']),
                    'label': result['recipe']['label'],
                    'image': result['recipe']['image']}} for result in response['hits']]

        hit_choice = request.POST.get('hit_choice')
        if hit_choice is not None and len(hits)>0:
            recipe_id = hits[int(hit_choice)]['recipe']['uri'].split('_')[-1]
            recipe_info = get_recipe_info(request, recipe_id)
            context = {'img': img, 'form': form, 'recognized_class': recognized_class, 'hits': hits, 'recipe_info': recipe_info}
            return render(request, 'loginstate/home.html', context)
        
        else:
            form = ImageForm()

        # Get the latest uploaded image object
        img = ImageUpload.objects.last()

    context = {'img': img, 'form': form, 'recognized_class': recognized_class, 'hits': hits}
    return render(request, 'loginstate/home.html', context)

@login_required(login_url='login')
def chatbot(request):
    return render(request, 'chatbot.html')

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