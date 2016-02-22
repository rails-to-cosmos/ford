"""
Django settings for force project.

Generated by 'django-admin startproject' using Django 1.9.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
from os.path import abspath, basename, dirname, join, normpath

import dj_database_url

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# DJANGO_ROOT = dirname(dirname(abspath(__file__)))
# SITE_ROOT = dirname(DJANGO_ROOT)
# SITE_NAME = basename(DJANGO_ROOT)
PROJECT_PATH = os.path.realpath(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'jsw!n15v(o^s3r+12%1==rof^#e-v1tq5g%=qvctkcs0+)j&&i'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'pipeline',
    'menu',
    'authorization',
    'rest_framework',
]

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = normpath(join(BASE_DIR, '.static'))
STATICFILES_DIRS = (
    'static',
    'node_modules',
)
STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'pipeline.finders.PipelineFinder',
)

PIPELINE = {
    'JS_COMPRESSOR': 'pipeline.compressors.yuglify.YuglifyCompressor',
    'JAVASCRIPT': {
        'site-packages': {
            'source_filenames': (
                'react/dist/react-with-addons.js',
                'react-dom/dist/react-dom.js',
                'react-bootstrap/dist/react-bootstrap.min.js',
                'jquery/dist/jquery.min.js',
            ),
            'output_filename': 'site-packages.js',
        },
        'force': {
            'source_filenames': (
                'js/NavigationBar.jsx',
            ),
            'output_filename': 'force.js',
        },
        'authorization': {
            'source_filenames': (
                'AuthorizationForm.jsx',
            ),
            'output_filename': 'authorization.js'
        },
        'menu': {
            'source_filenames': (
                'js/ProductList.jsx',
            ),
            'output_filename': 'menu.js'
        }
    },
    'CSS_COMPRESSOR': 'pipeline.compressors.yuglify.YuglifyCompressor',
    'STYLESHEETS': {
        'site-packages': {
            'source_filenames': (
                'bootstrap/dist/css/bootstrap.min.css',
            ),
            'output_filename': 'force.css',
        },
        'force': {
            'source_filenames': (
                'css/app.css',
            ),
            'output_filename': 'force.css',
        },
        'authorization': {
            'source_filenames': (
                'authorization.css',
            ),
            'output_filename': 'authorization.css',
        },
        'menu': {
            'source_filenames': (
                'css/menu.css',
            ),
            'output_filename': 'menu.css',
        },
    },
    'COMPILERS': (
        'react.utils.pipeline.JSXCompiler',
        # 'pipeline_browserify.compiler.BrowserifyCompiler'
    ),
}

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'pipeline.middleware.MinifyHTMLMiddleware',
]

ROOT_URLCONF = 'force.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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

WSGI_APPLICATION = 'force.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Parse database configuration from $DATABASE_URL
DATABASES['default'] = dj_database_url.config()

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']
