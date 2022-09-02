from django.contrib.auth.models import AbstractUser
from multiselectfield import MultiSelectField
from django.db import models

# Create your models here.
class CustomUser(AbstractUser):
	ALLERGIES = (
		('Celery','Sedano'),
		('Crustacean','Crostacei'),
		('Dairy','Lattosio'),
		('Eggs','Uova'),
		('Fish','Pesce'),
		('Gluten','Glutine'),
		('Lupine','Lupini'),
		('Mustard','Senape'),
		('Peanut','Arachidi'),
		('Sesame','Sesamo'),
		('Shellfish','Molluschi'),
		('Soy','Soia'),
		('Tree-nut','Noci'),
		('Wheat','Frumento')
		)

	DIETS = (
		('Alcohol-free','No alcool'),
		('Balanced','Bilanciata'),
		('High-Fiber','Molte fibre'),
		('High-Protein','Molte proteine'),
		('Keto','Chetogenica'),
		('Kidney friendly','Per i reni'),
		('Kosher','Kosher'),
		('Low-Carb','Pochi carboidrati'),
		('Low-Fat','Pochi grassi'),
		('Low potassium','Poco potassio'),
		('Low-Sodium','Povera di sodio'),
		('No oil added','Senza olio aggiunto'),
		('No-sugar','Senza zuccheri'),
		('Paleo','Paleolitica'),
		('Pescatarian','Pescetariana'),
		('Pork-free','Senza carne di maiale'),
		('Red meat-free','Senza carne rossa'),
		('Sugar-conscious','Pochi zuccheri'),
		('Vegan','Vegana'),
		('Vegetarian','Vegetariana')
		)


	diets = MultiSelectField(choices=DIETS, blank=True)
	allergies = MultiSelectField(choices=ALLERGIES, blank=True)

	def __str__(self):
		return self.username

class ImageUpload(models.Model):
	picture = models.ImageField(null=True, blank=True)