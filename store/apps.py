from django.apps import AppConfig


class StoreConfig(AppConfig):
	default_auto_field = 'django.db.models.BigAutoField'
	name = 'store'

	def ready(self):
		"""Import signals when app is ready"""
		import store.signals  # replace with your actual app name