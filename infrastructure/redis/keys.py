from infrastructure.redis.namespaces import NameSpaces
from infrastructure.redis.generate_key import generate_cache_key


# =========================================================
# SESSION CACHE KEYS
# =========================================================
class SessionCacheKeys:

    @staticmethod
    def single_session(session_id: str, is_prefix: bool = False):
        return (
            f"{NameSpaces.SESSIONS}:single"
            if is_prefix
            else f"{NameSpaces.SESSIONS}:single:{session_id}"
        )

    @staticmethod
    def sessions_list(query=None, is_prefix: bool = False):
        if is_prefix:
            return f"{NameSpaces.SESSIONS}:list"

        return generate_cache_key(NameSpaces.SESSIONS, "list", query or {})

    @staticmethod
    def user_sessions(user_id: str, query=None, is_prefix: bool = False):
        if is_prefix:
            return f"{NameSpaces.SESSIONS}:list-user:{user_id}"

        return generate_cache_key(
            NameSpaces.SESSIONS,
            f"list-user:{user_id}",
            query or {}
        )

    @staticmethod
    def user_single_session(user_id: str, session_id: str = None, is_prefix: bool = False):
        if is_prefix:
            return f"{NameSpaces.SESSIONS}:single-user:{user_id}"

        return f"{NameSpaces.SESSIONS}:single-user:{user_id}:{session_id}"


# =========================================================
# USER NOTIFICATION CACHE KEYS
# =========================================================
class UserNotificationCacheKeys:

    @staticmethod
    def user_notification_options(user_id: str, is_prefix: bool = False):
        if is_prefix:
            return f"{NameSpaces.USERS_NOTIFICATION_OPTIONS}:single"

        return f"{NameSpaces.USERS_NOTIFICATION_OPTIONS}:single:{user_id}"

    @staticmethod
    def user_notification_options_list(query=None, is_prefix: bool = False):
        if is_prefix:
            return f"{NameSpaces.USERS_NOTIFICATION_OPTIONS}:list"

        return generate_cache_key(
            NameSpaces.USERS_NOTIFICATION_OPTIONS,
            "list",
            query or {}
        )


# =========================================================
# USER DEVICE CACHE KEYS
# =========================================================
class UserDeviceCacheKeys:

    @staticmethod
    def user_base_device(user_id: str, is_prefix: bool = False):
        if is_prefix:
            return f"{NameSpaces.USER_DEVICE}:single"

        return f"{NameSpaces.USER_DEVICE}:single:{user_id}"

    @staticmethod
    def user_base_devices(user_id: str, query=None, is_prefix: bool = False):
        if is_prefix:
            return f"{NameSpaces.USER_DEVICE}:user-base:{user_id}"

        return generate_cache_key(
            NameSpaces.USER_DEVICE,
            f"user-base:{user_id}",
            query or {}
        )

    @staticmethod
    def users_devices_list(query=None, is_prefix: bool = False):
        if is_prefix:
            return f"{NameSpaces.USER_DEVICE}:list"

        return generate_cache_key(
            NameSpaces.USER_DEVICE,
            "list",
            query or {}
        )


# =========================================================
# USERS CACHE KEYS
# =========================================================
class UsersCacheKeys:

    @staticmethod
    def users_list(query=None, is_prefix: bool = False):
        if is_prefix:
            return f"{NameSpaces.USERS}:list"

        return generate_cache_key(NameSpaces.USERS, "list", query or {})

    @staticmethod
    def users_single(user_id: str, is_prefix: bool = False):
        if is_prefix:
            return f"{NameSpaces.USERS}:single"

        return f"{NameSpaces.USERS}:single:{user_id}"
    
    # @staticmethod
    # def user_sessions(user_id: str, is_prefix: bool = False, query:dict =None):
    #     if is_prefix:
    #         return f"{NameSpaces.USERS}:userbase:{user_id}"

    #     return generate_cache_key(NameSpaces.USERS, f"userbase:{user_id}", query or {})
        

    @staticmethod
    def users_list_for_dropdown(query=None, is_prefix: bool = False):
        if is_prefix:
            return f"{NameSpaces.USERS}:list-dropdown"

        return generate_cache_key(
            NameSpaces.USERS,
            "list-dropdown",
            query or {}
        )


# =========================================================
# FILE CACHE KEYS
# =========================================================
class FileCacheKeys:

    @staticmethod
    def file_single(file_id, is_prefix: bool = False):
        if is_prefix:
            return f"{NameSpaces.FILES}:single"

        return f"{NameSpaces.FILES}:single:{file_id}"

    @staticmethod
    def user_files(uploader_id: str, query=None, is_prefix: bool = False):
        if is_prefix:
            return f"{NameSpaces.FILES}:list-user:{uploader_id}"

        return generate_cache_key(
            NameSpaces.FILES,
            f"list-user:{uploader_id}",
            query or {}
        )

    @staticmethod
    def files_list(query=None, is_prefix: bool = False):
        if is_prefix:
            return f"{NameSpaces.FILES}:list"

        return generate_cache_key(NameSpaces.FILES, "list", query or {})


# =========================================================
# OTP CACHE KEYS
# =========================================================
class OtpCacheKeys:

    @staticmethod
    def forgot_password_otp(email: str, channel: str, is_prefix: bool = False):
        if is_prefix:
            return f"{NameSpaces.OTP}:forgot-password"

        return f"{NameSpaces.OTP}:forgot-password:{email}:{channel}"

    @staticmethod
    def otp_attempts_count(email: str):
        return f"{NameSpaces.OTP}:attempts-count:{email}"

    @staticmethod
    def otp_locked(email: str):
        return f"{NameSpaces.OTP}:locked:{email}"

    @staticmethod
    def reset_password_token(email: str):
        return f"{NameSpaces.OTP}:reset-token:{email}"