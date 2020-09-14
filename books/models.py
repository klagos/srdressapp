from django.db import models

# Create your models here.

class publicacion(models.Model):
	idPub = models.IntegerField()
	idUs = models.IntegerField()

class puntuacion(models.Model):
	idUs = models.IntegerField()
	idPub = models.IntegerField()
	punt = models.IntegerField()
