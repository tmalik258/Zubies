import os
from pathlib import Path
from django.urls import reverse_lazy
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent



# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")

DEBUG = True
# DEBUG_PROPAGATE_EXCEPTIONS = True

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # EXTERNAL PACKAGES
    "django_cleanup.apps.CleanupConfig",
    "django_countries",
    "mptt",
    "django_mptt_admin",
    'facebook_pixel_code',
	'django_seed',
    # INTERNAL APPS
    "account",
    "address",
    'basket',
    'checkout',
    "more",
    "order",
    "store",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "store.context_processors.navlist",
                "basket.context_processors.basket",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"



# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files and Media files (CSS, JavaScript, Images)

STATIC_URL = 'static/'
# STATIC_ROOT = [BASE_DIR / "static"]
STATICFILES_DIRS = [
	BASE_DIR / "static"
]

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGIN_REDIRECT_URL = reverse_lazy("store:index")
AUTH_USER_MODEL = "account.User"
LOGIN_URL = "/account/login"

PASSWORD_RESET_TIMEOUT_DAYS = 2

# Email Backend
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

# SMTP Configuration for Gmail
EMAIL_HOST = "smtp.gmail.com"  # or the SMTP server provided by your email service
EMAIL_PORT = 587  # or the appropriate port for your email service
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")  # your Gmail or email service username
EMAIL_HOST_PASSWORD = os.getenv(
    "EMAIL_HOST_PASSWORD"
)  # your Gmail or email service password
EMAIL_USE_TLS = True  # or False if your email service does not support TLS/SSL
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


# Sessions IDs
BASKET_SESSION_ID = "basket"
BILLING_ADDRESS_SESSION_ID = "billing_address"
DELIVERY_CHARGES_SESSION_ID = 'delivery_charges'


# Facebook ID
# FACEBOOK_PIXEL_CODE_ID = os.getenv("FACEBOOK_PIXEL_CODE_ID")
