import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url
from django.contrib.messages import constants as messages
from django.core.management.utils import get_random_secret_key

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'l0yw5&ox2!+68*lx#*6w5uev_()njueg%q$8n_!cnyi&nf8fd2')

DEBUG = False

ALLOWED_HOSTS = ['librarymanagement.online', 'www.librarymanagement.online']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
    'books',
    'crispy_forms',
    'crispy_bootstrap5',
    'widget_tweaks',
    'administration',
    'home',
]

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'library_web_system.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'library_web_system.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# if DEBUG:
#     #  print("debug true")
#      DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.sqlite3',
#             'NAME': BASE_DIR / 'db.sqlite3',
#         }
#         # 'default' : dj_database_url.parse(DATABASE_URL)
#     }
# else:

#     # print("debug false ")
#     DATABASES = {
#         # 'default': {
#         #     'ENGINE': 'django.db.backends.sqlite3',
#         #     'NAME': BASE_DIR / 'db.sqlite3',
#         # }
#         'default' : dj_database_url.parse(DATABASE_URL)
#     }


# if (os.environ.get("PRODUCTION") == "PRODUCTION"):
#     print("ONLINE TOH")
#     DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'DB_NAME',
#         'USER': 'DB_USER',
#         'PASSWORD': 'DB_PASSWORD',
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
# }
# else:
    # print("SQLITE 3")
#DATABASES = {
#        'default': {
#            'ENGINE': 'django.db.backends.sqlite3',
#            'NAME': BASE_DIR / 'db.sqlite3',
#        }
#   }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'lmsdatabase',  # Replace with your actual database name
        'USER': 'Lms',  # Replace with your actual username
        'PASSWORD': '',  # Replace with your actual password
        'HOST': 'localhost',  # Adjust as necessary, typically 'localhost' or the actual host IP
        'PORT': '5432',  # Default PostgreSQL port
    }
}

#DATABASES = {
    #    'default': {
    #        'ENGINE': 'django.db.backends.mysql',
    #        'NAME': 'lms',
    #        'USER': 'root',
    #        'PASSWORD': '',
    #        'HOST': 'localhost',  # Or your MySQL host
    #        'PORT': '3306',
    #    }
    #}
# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Manila'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


AUTH_USER_MODEL = "accounts.User"




STATIC_URL = '/static/'
# STATIC_ROOT =  os.path.join(BASE_DIR,'static')

MEDIA_URL = '/media/'


STATICFILES_DIRS = [
    BASE_DIR / 'static'
]




LOGIN_URL = 'login'
LOGIN_REDIRECT_URL= '/index/'
LOGOUT_REDIRECT_URL = 'login'


MESSAGE_TAGS = {
        messages.DEBUG: 'alert-secondary',
        messages.INFO: 'alert-info',
        messages.SUCCESS: 'alert-success',
        messages.WARNING: 'alert-warning',
        messages.ERROR: 'alert-danger',
 }


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST='smtp.hostinger.com'
EMAIL_HOST_USER='no-reply@learnbuilddesign.com'
EMAIL_HOST_PASSWORD='Welcome01!'
EMAIL_PORT=465
EMAIL_USE_SSL=True
EMAIL_USE_TLS=False
DEFAULT_FROM_EMAIL="Daniel Fajardo Public Library <no-reply@danielfajardolibrary.online>"