from pathlib import Path
from decouple import config
from datetime import timedelta
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/


# SECRET_KEY = config("SECRET_KEY", cast=str,
#                     default='django-insecure-dm*g^m1vz1b2p_ydl7h^r-^3pa1^8yd!l##x4%z3m$fk%xc_%-')
# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = config("DEBUG", cast=bool, default=True)


SECRET_KEY = 'django-insecure-dm*g^m1vz1b2p_ydl7h^r-^3pa1^8yd!l##x4%z3m$fk%xc_%-'
# SECURITY WARNING: keep the secret key used in production secret!
DEBUG=True
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'http', 'websocket']


# Application definition

INSTALLED_APPS = [
    #channels 
    "daphne",

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # packages
    "drf_yasg",
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',

    

    # social
    'oauth2_provider',
    'social_django',
    'drf_social_oauth2',

    "corsheaders",

    # local
    "user",
    "job",
    "payment",

]

ASGI_APPLICATION = 'config.asgi.application'
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': "channels.layers.InMemoryChannelLayer",
        # 'CONFIG': {
        #     "hosts": [('127.0.0.1', 6379)],
        # },
    },
}


CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://github.com",
]


CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_METHODS = [
    "GET",
    "PATCH",
    "POST",
    "PUT",
    "OPTIONS"
]

CORS_ALLOW_HEADERS = [
    'Accept',
    'Content-Type',
]

MIDDLEWARE = [
    
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # OAuth
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
        'drf_social_oauth2.authentication.SocialAuthentication',
    ],

    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],

    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20
}


SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=12),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=15),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": False,

    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": "",
    "AUDIENCE": None,
    "ISSUER": None,
    "JSON_ENCODER": None,
    "JWK_URL": None,
    "LEEWAY": 0,

    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",

    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",

    "JTI_CLAIM": "jti",

    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),

    "TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainPairSerializer",
    "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",
    "TOKEN_VERIFY_SERIALIZER": "rest_framework_simplejwt.serializers.TokenVerifySerializer",
    "TOKEN_BLACKLIST_SERIALIZER": "rest_framework_simplejwt.serializers.TokenBlacklistSerializer",
    "SLIDING_TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer",
    "SLIDING_TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer",
}
# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': config("DB_NAME", cast=str, default="crm"),
#         'USER': config("USER", cast=str, default="postgres"),
#         'PASSWORD': config("PASSWORD", cast=str, default="postgres"),
#         'HOST': config("HOST", cast=str, default="localhost"),
#         'PORT': config("PORT", cast=int, default=5432),
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Tashkent'

USE_I18N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = config("EMAIL_HOST")
# EMAIL_HOST_USER = config("EMAIL_HOST_USER")
# EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
# EMAIL_PORT = config("EMAIL_PORT")
# EMAIL_USE_TLS = config("EMAIL_USE_TLS")
# EMAIL_SEND_USER = config("EMAIL_SEND_USER")

SITE_ID = 1
AUTH_USER_MODEL = 'user.User'


AUTHENTICATION_BACKENDS = (
    # Google
    'social_core.backends.google.GoogleOAuth2',
    # Google OpenID
    'drf_social_oauth2.backends.GoogleIdentityBackend',
    # Facebook
    'social_core.backends.facebook.FacebookAppOAuth2',
    'social_core.backends.facebook.FacebookOAuth2',
    # Github
    'social_core.backends.github.GithubOAuth2',
    #Instagram
    'social_core.backends.instagram.InstagramOAuth2',
    # Drf-social-oauth2
    'drf_social_oauth2.backends.DjangoOAuth2',
    # Django
    'django.contrib.auth.backends.ModelBackend',
)

# facebook
SOCIAL_AUTH_FACEBOOK_KEY = ''
SOCIAL_AUTH_FACEBOOK_SECRET = ''
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
SOCIAL_AUTH_FACEBOOK_FROFILE_EXTRA_PARAMS = {
    'fields' : 'id, name, email'
}

# Google
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = config("SOCIAL_AUTH_GOOGLE_OAUTH2_KEY")
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = config("SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET")
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile'
]

GOOGLE_ID_TOKEN_INFO_URL = 'https://www.googleapis.com/oauth2/v3/tokeninfo'
GOOGLE_ACCESS_TOKEN_OBTAIN_URL = 'https://oauth2.googleapis.com/token'
GOOGLE_USER_INFO_URL = 'https://www.googleapis.com/oauth2/v3/userinfo'


# Github
SOCIAL_AUTH_GITHUB_KEY = config("SOCIAL_AUTH_GITHUB_KEY")
SOCIAL_AUTH_GITHUB_SECRET = config("SOCIAL_AUTH_GITHUB_SECRET")

# instagram
SOCIAL_AUTH_INSTAGRAM_KEY = ''
SOCIAL_AUTH_INSTAGRAM_SECRET = ''
SOCIAL_AUTH_INSTAGRAM_AUTH_EXTRA_ARGUMENTS = {'scope' : 'likes comments relationships'}


#  Access Token Expiration
OAUTH2_PROVIDER = {
    'ACCESS_TOKEN_EXPIRE_SECONDS': 604800,  # 7 days
}

# 3600 (1 hour)
# 36000 x 24 = 86400 (1 days)
# 86400 x 7 = 604800 (7 days)


SOCIAL_AUTH_PIPELINE = (
  'social_core.pipeline.social_auth.social_details',
  'social_core.pipeline.social_auth.social_uid',
  'social_core.pipeline.social_auth.auth_allowed',
  'social_core.pipeline.social_auth.social_user',
  'social_core.pipeline.user.get_username',
  'social_core.pipeline.social_auth.associate_by_email',
  'social_core.pipeline.user.create_user',
  'social_core.pipeline.social_auth.associate_user',
  'social_core.pipeline.social_auth.load_extra_data',
  'social_core.pipeline.user.user_details',
)