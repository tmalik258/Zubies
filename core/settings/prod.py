from .base import *

ALLOWED_HOSTS = ['.vercel.app', '.now.sh']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get("POSTGRES_DATABASE"),
        'USER': os.environ.get("POSTGRES_USER"),
        'PASSWORD': os.environ.get("POSTGRES_PASSWORD"),
        'HOST': os.environ.get("POSTGRES_HOST"),
        'PORT': os.environ.get("DB_PORT", 5432),
    }
}


STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')