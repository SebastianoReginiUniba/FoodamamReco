from django.contrib.auth.models import AbstractUser
from multiselectfield import MultiSelectField
from django.db import models

# Create your models here.
class CustomUser(AbstractUser):
	ALLERGIES = (
		('Celery','Celery'),
		('Crustacean','Crustacean'),
		('Dairy','Dairy'),
		('Eggs','Eggs'),
		('Fish','Fish'),
		('Gluten','Gluten'),
		('Lupine','Lupine'),
		('Mustard','Mustard'),
		('Peanut','Peanut'),
		('Sesame','Sesame'),
		('Shellfish','Shellfish'),
		('Soy','Soy'),
		('Tree-nut','Tree nuts'),
		('Wheat','Wheat')
		)

	DIETS = (
		('Alcohol-free','No alcohol'),
		('Balanced','Balanced'),
		('High-Fiber','More fibers'),
		('High-Protein','More proteins'),
		('Keto','Ketogenic'),
		('Kidney friendly','Kidney friendly'),
		('Kosher','Kosher'),
		('Low-Carb','Low carbs'),
		('Low-Fat','Low fats'),
		('Low potassium','Low potassium'),
		('Low-Sodium','Low sodium'),
		('No oil added','No oil added'),
		('No-sugar','No sugar'),
		('Paleo','Paleolithic'),
		('Pescatarian','Pescatarian'),
		('Pork-free','No pork'),
		('Red meat-free','No red meat'),
		('Sugar-conscious','Beware of sugar'),
		('Vegan','Vegan'),
		('Vegetarian','Vegetarian')
		)


	diets = MultiSelectField(choices=DIETS, blank=True)
	allergies = MultiSelectField(choices=ALLERGIES, blank=True)
	def __str__(self):
		return self.username

# utils.py
from loginstate.models import CustomUser

ALLERGIES_DICT = {allergy[0]: allergy[0] for allergy in CustomUser.ALLERGIES}
DIETS_DICT = {diet[0]: diet[0] for diet in CustomUser.DIETS}

class ImageUpload(models.Model):
	picture = models.ImageField(null=True, blank=True)