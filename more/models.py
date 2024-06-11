from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.

class NewsLetter(models.Model):
	email = models.EmailField()

	def __str__(self):
		return self.email
