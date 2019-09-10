import os
import environ

env = environ.Env(DEBUG=(bool, False), GS_BUCKET_NAME=(str, None))

env.read_env(os.environ.get("ENV_PATH", ".env"))

root = environ.Path(__file__) - 3
SITE_ROOT = root()

DEBUG = env("DEBUG")
TEMPLATE_DEBUG = DEBUG

SECRET_KEY = env("SECRET_KEY")

ALLOWED_HOSTS = [os.environ.get("CURRENT_HOST", "localhost"), "127.0.0.1"]

# Enable Django security precautions if *not* running locally
if "0.0.0.0" not in ALLOWED_HOSTS:
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_HSTS_PRELOAD = True
    SECURE_HSTS_SECONDS = 3600
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    X_FRAME_OPTIONS = "DENY"


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "unicodex",
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

STATIC_ROOT = "/static/"

GS_BUCKET_NAME = env("GS_BUCKET_NAME", None)
if GS_BUCKET_NAME:
    DEFAULT_FILE_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
    STATICFILES_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
    GS_DEFAULT_ACL = "publicRead"

    STATIC_HOST = "https://storage.googleapis.com/{GS_BUCKET_NAME}/"
    STATIC_URL = f"{STATIC_HOST}/{STATIC_ROOT}"
    MEDIA_ROOT = STATIC_HOST + "media/"
    MEDIA_URL = STATIC_HOST + "media/"

    INSTALLED_APPS += ["storages"]
else:
    DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"

    STATIC_HOST = "/"
    STATIC_URL = "/static/"

    MEDIA_ROOT = "media/"  # where files are stored on the local FS (in this case)
    MEDIA_URL = "/media/"  # what is prepended to the image URL (in this case)


ROOT_URLCONF = "unicodex.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

WSGI_APPLICATION = "unicodex.wsgi.application"

DATABASES = {"default": env.db()}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True