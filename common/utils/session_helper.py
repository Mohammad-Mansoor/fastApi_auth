from fastapi import Request
from typing import Optional
from datetime import datetime, timedelta

from modules.sessions.schema import CreateSession
from modules.sessions.models import SessionSourceTypes
from core.config import settings
from modules.usersDevices.schema import AddDevice


class SessionHelper:

    @staticmethod
    def get_ip_address(request: Request) -> str:
        """
        Extract real client IP address.
        Supports proxies/load balancers.
        """

        forwarded_for = request.headers.get("x-forwarded-for")

        if forwarded_for:
            # Client IP is first in list
            return forwarded_for.split(",")[0].strip()

        if request.client:
            return request.client.host

        return "unknown"

    @staticmethod
    def get_user_agent(request: Request) -> str:
        """
        Extract browser user-agent string.
        """

        return request.headers.get("user-agent", "unknown")

    @staticmethod
    def get_fingerprint(request: Request) -> str:
        return request.headers.get("x-fingerprint", "")

    @staticmethod
    def get_device_name(request: Request) -> str:
        return request.headers.get("x-device-name", "Unknown Device")

    @staticmethod
    def get_device_type(request: Request) -> str:
        return request.headers.get("x-device-type", "unknown")

    @staticmethod
    def get_os(request: Request) -> str:
        return request.headers.get("x-os", "unknown")

    @staticmethod
    def get_browser(request: Request) -> str:
        return request.headers.get("x-browser", "unknown")

    @staticmethod
    def get_source(request: Request) -> SessionSourceTypes:
        """
        web / mobile / desktop
        """

        source = request.headers.get("x-source", "web")

        try:
            return SessionSourceTypes(source)
        except Exception:
            return SessionSourceTypes.web

    @staticmethod
    def get_device_id(request: Request) -> str:
        """
        Device ID can be same as fingerprint for now.
        """

        return request.headers.get("x-fingerprint", "")
    
    @staticmethod
    def get_device_id_from_cookies(request:Request):
        return request.cookies.get("device_id")

    @staticmethod
    def build_session_payload(
        request: Request,
        user_id,
        refresh_token: str,
        refresh_days: int = settings.REFRESH_TOKEN_EXPIRE_DAYS,
    ) -> CreateSession:
        """
        Create ready-to-save session payload.
        """

        now = datetime.utcnow()

        return CreateSession(
            userId=user_id,
            refreshToken=refresh_token,

            ipAddress=SessionHelper.get_ip_address(request),
            userAgent=SessionHelper.get_user_agent(request),

            deviceId=SessionHelper.get_device_id(request),
            deviceName=SessionHelper.get_device_name(request),
            deviceType=SessionHelper.get_device_type(request),

            os=SessionHelper.get_os(request),
            browser=SessionHelper.get_browser(request),

            source=SessionHelper.get_source(request),

            fingerprint=SessionHelper.get_fingerprint(request),

            isValid=True,

            lastActiveAt=now,
            expiresAt=now + timedelta(days=refresh_days),
        )
        
    @staticmethod
    def build_device_payload(session_payload:dict):
        print("this is device paylaod💕💕💕", session_payload)
        device_payload = AddDevice(
            userId = str(session_payload.userId),
            deviceId= session_payload.deviceId,
            deviceName= session_payload.deviceName,
            deviceType= session_payload.deviceType,
            os= session_payload.os,
            source=session_payload.source,
            fingerprint= session_payload.fingerprint,
            userAgent= session_payload.userAgent,
            browser= session_payload.browser,
            lastIp= session_payload.ipAddress,
        )
        return device_payload