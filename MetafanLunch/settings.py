"""
Django settings for MetafanLunch project.

Generated by 'django-admin startproject' using Django 5.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os
import jdatetime
import locale
from celery.schedules import crontab

# static files:
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticroot")
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "staticfiles"),
]

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

AUTH_USER_MODEL = "lunch.CustomUser"
LOGIN_URL = "/panel/login/"
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


LANGUAGE_CODE = "fa-ir"
locale.setlocale(locale.LC_ALL, "fa_IR")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-pr6b=5^i$pi5gx42-zgvjrlp@++uo2x+juee#1z%z7@k(f5yg@"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["npanel.metafan.info", "127.0.0.1"]
CSRF_TRUSTED_ORIGINS = ["https://npanel.metafan.info"]
CSRF_COOKIE_DOMAIN = "npanel.metafan.info"

# Application definition

INSTALLED_APPS = [
    # "unfold",
    "crispy_forms",
    "crispy_bootstrap4",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "lunch",
    "django_jalali",
    "surveys",
    "sqlite3",
    "messaging",
    "pwa",
    "attendance",
]

CRISPY_TEMPLATE_PACK = "bootstrap4"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
]

ROOT_URLCONF = "MetafanLunch.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "attendance.context_processors.site_info",
            ],
        },
    },
]

WSGI_APPLICATION = "MetafanLunch.wsgi.application"

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    # {
    #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    # },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "fa-ir"

TIME_ZONE = "Asia/Tehran"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


VAPID_PUBLIC_KEY = "BOIB34wIndy_DQ3rUBIQfcP5PTLoiH7ux8ztyjxGBngsVHSn57fK8hTaOKVX_51KV3Uz9Nm7Gw7oGLwmIGMNUFI"
VAPID_PRIVATE_KEY = ("OGB9YwZ8HQiwlVRX1y19FnqEl-S1IEA8yRHo7wljEag",)
VAPID_ADMIN_EMAIL = "info@metafan.info"


PWA_APP_NAME = "پنل متافن"
PWA_APP_DESCRIPTION = "سامانه یکپارچه متافن"
PWA_APP_THEME_COLOR = "#d4f1f7"
PWA_APP_BACKGROUND_COLOR = "#ffffff"
PWA_APP_DISPLAY = "standalone"
PWA_APP_SCOPE = "/"
PWA_APP_ORIENTATION = "portrait"
PWA_APP_START_URL = "/"
PWA_APP_STATUS_BAR_COLOR = "default"
PWA_APP_ICONS = [
    {"src": "/static/pwa/android/android-launchericon-512-512.png", "sizes": "512x512"}
]
PWA_APP_ICONS_APPLE = [{"src": "/static/pwa/ios/512.png", "sizes": "512x512"}]
PWA_APP_SPLASH_SCREEN = [
    {"src": "/static/pwa/windows11/SplashScreen.scale-100.png", "sizes": "620x300"},
    {"src": "/static/pwa/windows11/SplashScreen.scale-125.png", "sizes": "775x375"},
    {"src": "/static/pwa/windows11/SplashScreen.scale-150.png", "sizes": "930x450"},
    {"src": "/static/pwa/windows11/SplashScreen.scale-200.png", "sizes": "1240x600"},
    {"src": "/static/pwa/windows11/SplashScreen.scale-400.png", "sizes": "2480x1200"},
]
PWA_APP_DIR = "rtl"
PWA_APP_LANG = "fa-IR"
# PWA_APP_SHORTCUTS = [
#     {
#         "name": "Shortcut",
#         "url": "/target",
#         "description": "Shortcut to a page in my application",
#     }
# ]
# PWA_APP_SCREENSHOTS = [
#     {
#         "src": "/static/images/icons/splash-750x1334.png",
#         "sizes": "750x1334",
#         "type": "image/png",
#     }
# ]


# LOGGING = {
#     "version": 1,
#     "disable_existing_loggers": False,
#     "handlers": {
#         "file": {
#             "level": "DEBUG",
#             "class": "logging.FileHandler",
#             "filename": os.path.join(BASE_DIR, "debug.log"),
#             "encoding": "utf-8",
#         },
#     },
#     "loggers": {
#         "django": {
#             "handlers": ["file"],
#             "level": "DEBUG",
#             "propagate": True,
#         },
#     },
# }
