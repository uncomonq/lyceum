import importlib
from pathlib import Path

from decouple import config
from django.utils.translation import gettext_lazy as _

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

DEFAULT_USER_IS_ACTIVE = config(
    "DJANGO_DEFAULT_USER_IS_ACTIVE",
    default=DEBUG,
    cast=bool,
)

MAX_AUTH_ATTEMPTS = config(
    "DJANGO_MAX_AUTH_ATTEMPTS",
    default=3,
    cast=int,
)

BIRTHDAY_USERS_LIMIT = config(
    "BIRTHDAY_USERS_LIMIT",
    default=3,
    cast=int,
)

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
    "about.apps.AboutConfig",
    "catalog.apps.CatalogConfig",
    "core.apps.CoreConfig",
    "download.apps.DownloadConfig",
    "feedback.apps.FeedbackConfig",
    "homepage.apps.HomepageConfig",
    "rating.apps.RatingConfig",
    "users.apps.UsersConfig",
    "django_cleanup.apps.CleanupConfig",
]

DJANGO_MAIL = config("DJANGO_MAIL", default="noreply@example.com")

EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = BASE_DIR / "send_mail"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "users.middleware.LoadUserMiddleware",
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
                "users.context_processors.birthday_users",
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

LANGUAGE_CODE = "ru-ru"

LANGUAGES = [
    ("ru-ru", _("Russian")),
    ("en-us", _("English")),
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
STATIC_ROOT = BASE_DIR / "static"

LOGIN_URL = "users:login"

LOGIN_REDIRECT_URL = "users:profile"

LOGOUT_REDIRECT_URL = "users:login"

AUTHENTICATION_BACKENDS = [
    "users.backends.UserAuthBackend",
]
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
