from .base import *

ALLOWED_HOSTS = ['*']

DATABASES = {
	# Postgresql
    # 'default': {
    #     'ENGINE': 'django.db.backends.postgresql_psycopg2',
    #     'NAME': os.environ.get("DB_DATABASE"),
    #     'USER': os.environ.get("DB_USER"),
    #     'PASSWORD': os.environ.get("DB_PASSWORD"),
    #     'HOST': os.environ.get("DB_HOST"),
    #     'PORT': os.environ.get("DB_PORT", 5432),
    # }

	'default': {
        'ENGINE': 'mysql.connector.django',
        'NAME': os.environ.get("DB_NAME"),
        'USER': os.environ.get("DB_USER"),
        'PASSWORD': os.environ.get("DB_PASSWORD"),
        'HOST': os.environ.get("DB_HOST"),
        'PORT': os.environ.get("DB_PORT"),
        'OPTIONS': {
            'unix_socket': '/var/lib/mysql/mysql.sock',  # SHOW VARIABLES LIKE 'socket';
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}


STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

ADMINS = ['talhamalik25.tm@gmail.com']

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True