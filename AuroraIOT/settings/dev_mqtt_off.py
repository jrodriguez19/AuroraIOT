from .common import *

logger.info("Using MQTT_OFF settings")

# Activate or deactivate MQTT operation
MQTT_ACTIVE = False
logger.info(f"MQTT active status is: {MQTT_ACTIVE}")

DEBUG = False

ALLOWED_HOSTS = ["*"]


# Adding Django Debug Tool bar
# Check if django-debug-toolbar package is installed without making the actual import of 'debug_toolbar'
import importlib.util

if importlib.util.find_spec("debug_toolbar"):
    INSTALLED_APPS.append("debug_toolbar")

    """The order of MIDDLEWARE is important. You should include the Debug Toolbar middleware as early as possible in the list. 
    However, it must come after any other middleware that encodes the response’s content, such as GZipMiddleware."""
    MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")
else:
    import sys

    sys.exit(
        "Error: Module 'debug_toolbar' not found, please install with 'pipenv install --dev django-debug-toolbar'. Terminating application"
    )


# MQTT Config
MQTT_SERVER = config("MQTT_SERVER_DEV")
MQTT_PORT = config("MQTT_PORT_DEV")
MQTT_CLIENT_ID = "id-mqttclient-django-development"
MQTT_USER = config("MQTT_USER_DEV")
MQTT_PASSWORD = config("MQTT_PASSWORD_DEV")
MQTT_KEEPALIVE = 60

# Timescaledb
DATABASES = {
    "default": {
        "ENGINE": "timescale.db.backends.postgresql",
        "NAME": "auroraiotdb",
        "USER": config("DB_USERNAME_DEV"),
        "PASSWORD": config("DB_PASSWORD_DEV"),
        "HOST": config("DB_HOST_DEV"),
        "PORT": config("DB_PORT_DEV"),
    }
}

# PostgreSQL
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": "auroraiotdb",
#         "USER": config('DB_USERNAME_PROD'),
#         "PASSWORD": config('DB_PASSWORD_PROD'),
#         "HOST": config('DB_HOST_PROD'),
#         "PORT": config('DB_PORT_PROD'),
#     }
# }


def show_toolbar(request):
    return True


DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": show_toolbar,
}
