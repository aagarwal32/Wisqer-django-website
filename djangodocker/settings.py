"""
Django settings for djangodocker project.

Generated by 'django-admin startproject' using Django 5.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""
import os
import sys
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = str(os.environ.get("DEBUG")) == "1"
ENV_ALLOWED_HOST=os.environ.get("ENV_ALLOWED_HOST")
ENV_ALLOWED_HOST_2=os.environ.get("ENV_ALLOWED_HOST_2")
ENV_ALLOWED_HOST_3=os.environ.get("ENV_ALLOWED_HOST_3")
ALLOWED_HOSTS = ['0.0.0.0', 'localhost', '127.0.0.1']
if all([ENV_ALLOWED_HOST, ENV_ALLOWED_HOST_2, ENV_ALLOWED_HOST_3]):
    ALLOWED_HOSTS.append(ENV_ALLOWED_HOST)
    ALLOWED_HOSTS.append(ENV_ALLOWED_HOST_2)
    ALLOWED_HOSTS.append(ENV_ALLOWED_HOST_3)

if not DEBUG:
    SECURE_SSL_REDIRECT=False
    SECURE_HSTS_SECONDS=31536000 # 1 year in seconds
    SECURE_HSTS_INCLUDE_SUBDOMAINS=True
    SECURE_BROWSER_XSS_FILTER=True
    SECURE_CONTENT_TYPE_NOSNIFF=True
    CSRF_COOKIE_SECURE = True  # Ensure the CSRF cookie is only sent over HTTPS
    SESSION_COOKIE_SECURE = True  # Ensure session cookies are also sent only over HTTPS

    CSRF_TRUSTED_ORIGINS = [
    'https://www.wisqer.com',
    'https://wisqer.com',
    ]

else:
    SECURE_SSL_REDIRECT=False


# Application definition
########################

INSTALLED_APPS = [
    "polls.apps.PollsConfig",
    "accounts.apps.AccountsConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "bootstrap5",
    "reversion",
    "storages",
    "rest_framework",
]

REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'wisqerbot': '6/h',
    },
}

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "djangodocker.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, 'templates')],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "djangodocker.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

DB_USERNAME=os.environ.get("POSTGRES_USER")
DB_PASSWORD=os.environ.get("POSTGRES_PASSWORD")
DB_DATABASE=os.environ.get("POSTGRES_DB")
DB_HOST=os.environ.get("POSTGRES_HOST")
DB_PORT=os.environ.get("POSTGRES_PORT")
DB_IS_AVAIL = all([
    DB_USERNAME,
    DB_PASSWORD,
    DB_DATABASE,
    DB_HOST,
    DB_PORT
])

DB_IGNORE_SSL=os.environ.get("DB_IGNORE_SSL") == "true"

if DB_IS_AVAIL and not DEBUG:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": DB_DATABASE,
            "USER": DB_USERNAME,
            "PASSWORD": DB_PASSWORD,
            "HOST": DB_HOST,
            "PORT": DB_PORT
        }
    }

    if not DB_IGNORE_SSL:
        DATABASES["default"]["OPTIONS"] = {
            "sslmode": "require"
        }

    
#print(DATABASES)

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "America/New_York"

USE_I18N = True

USE_TZ = True


# Email Handling
# https://pypi.org/project/Django-Verify-Email/
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_ID')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PW')
DEFAULT_FROM_EMAIL = 'noreply<no_reply@domain.com>'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "static/"

if DEBUG:
    STATICFILES_DIRS = [
        BASE_DIR / "polls/static",
        #BASE_DIR / "accounts/static",
    ]
else:
    STATICFILES_DIRS = [
        BASE_DIR / "polls/static",
        #BASE_DIR / "accounts/static",
        BASE_DIR / "staticfiles",
    ]
    STATIC_ROOT = BASE_DIR / "staticfiles-cdn"

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

if not DEBUG:
    from .cdn.conf import * # noqa

if "test" in sys.argv:
    # override static file storage when testing
    STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"
    DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"
    print("Using local static files and file storage for testing.")