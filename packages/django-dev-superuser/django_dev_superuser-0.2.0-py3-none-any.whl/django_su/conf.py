from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()
DEFAULTS = {
    "USERNAME_FIELD": User.USERNAME_FIELD,
    "USERNAME": "admin",
    "PASSWORD": "admin",
    "EXTRA_ARGS": {},
}
USER_CONFIG = getattr(settings, "DJANGO_SU_CONFIG", {})

# Configurable Settings
USERNAME_FIELD = USER_CONFIG.get("USERNAME_FIELD", DEFAULTS["USERNAME_FIELD"])
USERNAME = USER_CONFIG.get("USERNAME", DEFAULTS["USERNAME"])
PASSWORD = USER_CONFIG.get("PASSWORD", DEFAULTS["PASSWORD"])
EXTRA_ARGS = USER_CONFIG.get("EXTRA_ARGS", DEFAULTS["EXTRA_ARGS"])
