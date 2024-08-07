from .common import *

logger.info("Using MQTT_OFF settings")

# Activate or deactivate MQTT operation
MQTT_ACTIVE = False
logger.info(f"MQTT active status is: {MQTT_ACTIVE}")

DEBUG = False

ALLOWED_HOSTS = ["*"]


# MQTT Config
MQTT_SERVER = config("MQTT_SERVER_PROD")
MQTT_PORT = config("MQTT_PORT_PROD")
MQTT_CLIENT_ID = "id-mqttclient-django-production"
MQTT_USER = config("MQTT_USER_PROD")
MQTT_PASSWORD = config("MQTT_PASSWORD_PROD")
MQTT_KEEPALIVE = 60

# Timescaledb
DATABASES = {
    "default": {
        "ENGINE": "timescale.db.backends.postgresql",
        "NAME": "auroraiotdb",
        "USER": config("DB_USERNAME_PROD"),
        "PASSWORD": config("DB_PASSWORD_PROD"),
        "HOST": config("DB_HOST_PROD"),
        "PORT": config("DB_PORT_PROD"),
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
