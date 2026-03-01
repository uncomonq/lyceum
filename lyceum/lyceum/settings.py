import importlib
from pathlib import Path

from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = config("DJANGO_DEBUG", default=True, cast=bool)

DEBUG_TOOLBAR_AVAILABLE = importlib.util.find_spec("debug_toolbar") is not None

SECRET_KEY = config("DJANGO_SECRET_KEY", default="secret")

ALLOWED_HOSTS = [
    host.strip()
    for host in config(
        "DJANGO_ALLOWED_HOSTS",
        default="localhost,127.0.0.1",
    ).split(",")
    if host.strip()
]

ALLOW_REVERSE = config("DJANGO_ALLOW_REVERSE", default=True, cast=bool)

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "tinymce",
    "sorl.thumbnail",
    "django_cleanup.apps.CleanupConfig",
    "core.apps.CoreConfig",
    "about.apps.AboutConfig",
    "catalog.apps.CatalogConfig",
    "homepage.apps.HomepageConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "lyceum.middleware.ReverseRussianWordsMiddleware",
]

if DEBUG and DEBUG_TOOLBAR_AVAILABLE:
    INSTALLED_APPS += ["debug_toolbar"]
    MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")

    INTERNAL_IPS = [
        "127.0.0.1",
    ]

ROOT_URLCONF = "lyceum.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "lyceum.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    },
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation.MinimumLengthValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "CommonPasswordValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "NumericPasswordValidator"
        ),
    },
]

MEDIA_URL = "/media/"

MEDIA_ROOT = BASE_DIR / "media"

LANGUAGE_CODE = "ru"

LANGUAGES = [
    ("ru", "Русский"),
    ("en", "English"),
]

LOCALE_PATHS = [
    BASE_DIR / "locale",
]

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = "static/"

STATICFILES_DIRS = [
    BASE_DIR / "static_dev",
]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
