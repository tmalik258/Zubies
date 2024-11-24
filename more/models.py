from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import EmailValidator


class NewsLetter(models.Model):
	email = models.EmailField(unique=True, validators=[EmailValidator()])
	subscribed = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
			verbose_name = 'Newsletter Subscription'
			verbose_name_plural = 'Newsletter Subscriptions'
			ordering = ['-created_at']

	def __str__(self):
		return f"{self.email} ({'Active' if self.active else 'Inactive'})"
