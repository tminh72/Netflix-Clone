from pathlib import Path
import dj_database_url
import os

def get_list(text):
    return [item.strip() for item in text.split(",")]

def get_bool_from_env(name, default_value):
    """Retrieve and convert an environment variable to a boolean object.

    Accepted values are `true` (case-insensitive) and `1`, any other value resolves to `False`.
    """
    value = os.environ.get(name)
    if value is None:
        return default_value
    return value.lower() in ("true", "1")

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = get_bool_from_env("DEBUG", True)


ALLOWED_HOSTS = get_list(os.environ.get("ALLOWED_HOSTS", "localhost,127.0.0.1"))

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "django.contrib.postgres",

    "src.core",
    "src.tests"
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware'

]

ROOT_URLCONF = 'src.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'src.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DB_CONN_MAX_AGE = int(os.environ.get("DB_CONN_MAX_AGE", 600))

DATABASE_CONNECTION_DEFAULT_NAME = "default"
DATABASE_CONNECTION_REPLICA_NAME = "replica"

DATABASES = {
    DATABASE_CONNECTION_DEFAULT_NAME: dj_database_url.config(
        default="postgres://admin:admin@db:5432/netflix_clone",
        conn_max_age=DB_CONN_MAX_AGE,
    ),
    DATABASE_CONNECTION_REPLICA_NAME: dj_database_url.config(
        default="postgres://admin:admin@db:5432/netflix_clone",
        conn_max_age=DB_CONN_MAX_AGE,
        test_options={"MIRROR": DATABASE_CONNECTION_DEFAULT_NAME},
    ),
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {"min_length": 8},
    }
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
