from enum import Enum
from typing import Literal


# ==============================
# EVENT TYPES
# ==============================
class NotificationEventType(str, Enum):
    SESSION_REVOKED = "SESSION_REVOKED"
    NEW_DEVICE_LOGIN = "NEW_DEVICE_LOGIN"
    USER_REGISTERED = "USER_REGISTERED"
    PASSWORD_RESET = "PASSWORD_RESET"
    FORGOT_PASSWORD = "FORGOT_PASSWORD"


# ==============================
# CHANNEL TYPES
# ==============================
NotificationChannel = Literal[
    "email",
    "whatsapp",
    "telegram",
    "inapp",
    "socket"
]