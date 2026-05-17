from datetime import UTC, datetime
import uuid
from fastapi import Request
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from core.security import verify_password, create_access_token, create_refresh_token, verify_refresh_token
from infrastructure.redis.service import RedisCacheService, redis_service
from infrastructure.redis.keys import SessionCacheKeys, UsersCacheKeys, UserDeviceCacheKeys
from modules.auth.repository import AuthRepository
from modules.usersDevices.repository import UserDeviceRepository
from .schemas import LoginPayload
from core.schemas import Headers
from modules.users.repository import UserRepository
from modules.sessions.repository import SessionRepository
from core.exceptions.app_exception import AppException
from modules.sessions.schema import CreateSession
from modules.usersDevices.schema import AddDevice
from common.utils.session_helper import SessionHelper
from core.exceptions.app_exception import AppException
import asyncio



class AuthService:
    def __init__(self):
        self.userRepo = UserRepository()
        self.sessionRepo = SessionRepository()
        self.deviceRepo = UserDeviceRepository()
        self.redis_service = RedisCacheService()
        self.authRepo = AuthRepository()

    async def login(self, db:AsyncSession, data: LoginPayload, request: Request):
        user = await self.userRepo.get_user_by_email(db, data.email)
        print(user)

        if not user:
            raise AppException(status_code=400, message = "Invalid Email or password", error ="Invalid Email or password")

        if not verify_password(data.password, user.password):
            raise AppException(status_code=400, message = "Invalid Email or password", error ="Invalid Email or password")
        
        existing_device_id = SessionHelper.get_device_id_from_cookies(request)
        incoming_finger_print = SessionHelper.get_fingerprint(request)
        find_device = await self.deviceRepo.find_device(db, user.id, existing_device_id, incoming_finger_print)
        refresh_token_payload = {
            "userId": str(user.id)
        }
        refresh_token = create_refresh_token(refresh_token_payload)
        session_payload = SessionHelper.build_session_payload(
            request = request,
            user_id = user.id,
            refresh_token=refresh_token
        )
        device_payload = SessionHelper.build_device_payload(session_payload)

        if not find_device:
            device = await self.deviceRepo.add_device(db, device_payload)
            await db.flush()
            existing_device_id = str(uuid.uuid4())
            print("New Device Detected device_id❌❌❌", existing_device_id)
            #ALERT THE USER VIA PREFERED NOTIFICATION CHANNEL
        else:
            print("No New Device Detected device_id ✅✅✅", existing_device_id)
            #UPDATE THE DEVIEC INFO.
            ...
            
        session = await self.sessionRepo.create_session(db, session_payload)
        await db.flush()
        print("this is session info:🤣🤣🤣:", session)
        # device = await self.deviceRepo.add_device(db,device_payload)
        
        access_token_payload ={
            "userId": str(user.id),
            "sessionId": str(session.id)
        }
        access_token = create_access_token(access_token_payload)
        await db.commit()
        
        return {
            "refresh_token": refresh_token,
            "access_token": access_token,
            "device_id": existing_device_id
            
        }     
    async def me(self, db:AsyncSession, request:Request):
        user_id = request.state.userId
        cache_key = UsersCacheKeys.users_single(user_id)
        if not user_id:
            raise AppException(status_code=404, message= "Not Found", error= "NOT_FOUND")
        async def queryDB():
            user = await self.userRepo.get_user_by_id(db, user_id)
            json_user = jsonable_encoder(user)
            return json_user
        result = await self.redis_service.get_or_set(cache_key, queryDB)
        return result
    async def logout(self, db:AsyncSession, req:Request):
        user_id = req.state.userId
        session_id = req.state.sessionId
        cache_key = SessionCacheKeys.single_session(session_id)
        cache_key_user_list = SessionCacheKeys.user_sessions(user_id, {}, is_prefix=True)
        
        if not user_id or not session_id:
            raise AppException(status_code=400, message= "Invalid Logout Request", error= "TOKEN_NOT_AUTHORIZED")
        
        user = await self.userRepo.get_user_by_id(db, user_id)
        user_session = await self.sessionRepo.get_session_by_id(db, session_id)
        if not user or not user_session or str(user_session.userId) != user_id or not user_session.isValid:
            raise AppException(status_code=401, message= "No Active Session Found!", error="NO_ACTIVE_SESSION")
        now = datetime.now(UTC)
        user_session.isValid = False
        user_session.logoutAt = now
        user_session.lastActiveAt = now
        await db.commit()
        await asyncio.gather(
            # db.commit(),
            self.redis_service.del_by_prefix(cache_key_user_list),
            self.redis_service.del_key(cache_key)
        )
        return user_session     
    async def logout_all_sessions(self, db:AsyncSession, req:Request):
        user_id = getattr(req.state, "userId", None)
        session_id = getattr(req.state, "sessionId", None)
        cache_key = SessionCacheKeys.single_session(session_id, is_prefix=True)
        cache_key_user_list = SessionCacheKeys.user_sessions(user_id, {}, is_prefix=True)
        cache_key__list = SessionCacheKeys.sessions_list({}, is_prefix=True)
        if not user_id or not session_id:
            raise AppException(status_code=401, message="Invalid Logout Request", error="INVALID_LOGOUT_REQUEST")
        logout_sessions = await self.authRepo.logout_all_active_sessions_by_user_id(user_id,db)
        # we can emmit rabbitMQ events here 
        
        await db.commit()
        await asyncio.gather(
            self.redis_service.del_by_prefix(cache_key),
            self.redis_service.del_by_prefix(cache_key_user_list),
            self.redis_service.del_by_prefix(cache_key__list)
        )
        return logout_sessions
    async def logout_all_other_sessions(self, db:AsyncSession, req:Request):
        user_id = getattr(req.state, "userId", None)
        session_id = getattr(req.state, "sessionId", None)
        cache_key = SessionCacheKeys.single_session(session_id, is_prefix=True)
        cache_key_user_list = SessionCacheKeys.user_sessions(user_id, {}, is_prefix=True)
        cache_key__list = SessionCacheKeys.sessions_list({}, is_prefix=True)
        if not user_id or not session_id:
            raise AppException(status_code=401, message="Invalid Logout Request", error="INVALID_LOGOUT_REQUEST")
        logout_sessions = await self.authRepo.logout_other_sessions_except_current_by_user_id(user_id,session_id,db)
        # we can emmit rabbitMQ events here 
        
        await db.commit()
        await asyncio.gather(
            self.redis_service.del_by_prefix(cache_key),
            self.redis_service.del_by_prefix(cache_key_user_list),
            self.redis_service.del_by_prefix(cache_key__list)
        )
        return logout_sessions
    async def refresh_token(self, db:AsyncSession, req:Request):
        old_refresh_token = req.cookies.get("refresh_token")
        persistent_device_id = req.cookies.get("device_id")
        current_fingerprint = req.headers.get("x_fingerprint")
        now = datetime.now(UTC)

    
        # ------------------------------------------------------------
        # CASE:
        # No refresh token cookie was sent by client.
        #
        # POSSIBLE REASONS:
        # - User logged out
        # - Cookie expired
        # - Frontend bug
        # - Browser cleared cookies
        #
        # SECURITY LEVEL:
        # LOW
        #
        # ACTION:
        # - Do NOT revoke sessions
        # - Do NOT notify user
        # - Just deny refresh request
        #
        # RECOMMENDATION:
        # Log as INFO level only.
        # ------------------------------------------------------------
        if not old_refresh_token:
            print("No refresh token cookie was sent by client.")
            raise AppException(
                status_code=401,
                message="Invalid Refresh Token",
                error="INVALID_TOKEN"
            )
            

        jwt_payload = verify_refresh_token(old_refresh_token)
    

        # ------------------------------------------------------------
        # CASE:
        # JWT verification failed.
        #
        # POSSIBLE REASONS:
        # - Token expired
        # - Token tampered
        # - Invalid signature
        # - Corrupted token
        #
        # SECURITY LEVEL:
        # MEDIUM
        #
        # ACTION:
        # - Revoke CURRENT SESSION if identifiable
        # - Do NOT revoke all sessions yet
        # - Log security warning
        #
        # USER NOTIFICATION?
        # Usually NO.
        #
        # RECOMMENDATION:
        # Add audit/security log for monitoring repeated failures.
        # ------------------------------------------------------------
        if not jwt_payload:
            print("JWT verification failed.")
            raise AppException(
                status_code=401,
                message="Token invalid or already rotated",
                error="INVALID_TOKEN"
            )

        session = await self.authRepo.get_session_by_refresh_token(
            old_refresh_token,
            db
        )


        # ------------------------------------------------------------
        # CASE:
        # Refresh token not found in DB.
        #
        # THIS IS IMPORTANT.
        #
        # POSSIBLE REASONS:
        # - Token already rotated
        # - Replay attack
        # - Stolen refresh token
        # - Session revoked
        #
        # SECURITY LEVEL:
        # HIGH
        #
        # ACTION:
        # - Revoke ALL user sessions if possible
        # - Force re-login everywhere
        # - Create security event log
        #
        # USER NOTIFICATION?
        # YES — recommended.
        #
        # Example:
        # "We detected suspicious login/session activity.
        # Please login again."
        #
        # RECOMMENDATION:
        # This is where replay detection should happen.
        # ------------------------------------------------------------
        if not session:
            print("Refresh token not found in DB.")
            raise AppException(
              status_code=401,
                message="Token invalid or already rotated",
                error="INVALID_TOKEN"
            )

        cache_key = SessionCacheKeys.single_session(session.id, is_prefix=True)
        cache_key_user_list = SessionCacheKeys.user_sessions(
            session.userId,
            {},
            is_prefix=True
        )
        cache_key__list = SessionCacheKeys.sessions_list(
            {},
            is_prefix=True
        )


        # ------------------------------------------------------------
        # CASE:
        # JWT userId does not match DB session userId.
        #
      # POSSIBLE REASONS:
        # - Token manipulation
        # - Database inconsistency
        # - Severe attack attempt
        #
        # SECURITY LEVEL:
        # CRITICAL
        #
        # ACTION:
        # - Revoke ALL user sessions immediately
        # - Log CRITICAL security event
        # - Consider temporary account lock if repeated
        #
        # USER NOTIFICATION?
        # YES — strongly recommended.
        #
        # RECOMMENDATION:
        # Investigate if this ever happens in production.
        # This should almost NEVER happen normally.
        # ------------------------------------------------------------
        if str(session.userId) != jwt_payload.get("userId"):
            print("JWT userId does not match DB session userId.")
            raise AppException(
                status_code=401,
                message="Token invalid or already rotated",
                error="INVALID_TOKEN"
        )


        # ------------------------------------------------------------
        # CASE:
        # Device ID mismatch.
        #
        # POSSIBLE REASONS:
        # - Refresh token copied to another device
        # - Cookie theft
        # - Browser cloning
        #
        # SECURITY LEVEL:
        # HIGH
        #
        # ACTION:
        # - Revoke CURRENT SESSION
        # - Optionally revoke all sessions for banking/high-security apps
        #
        # USER NOTIFICATION?
        # YES — recommended.
        #
        # Example:
        # "A login attempt from another device was blocked."
        #
        # RECOMMENDATION:
        # Log IP address + device metadata.
        # ------------------------------------------------------------
        if session.deviceId != persistent_device_id:
            print("Device ID mismatch.")
            raise AppException(
                status_code=401,
                message="Token invalid or already rotated",
                error="INVALID_TOKEN"
            )


        # ------------------------------------------------------------
        # CASE:
        # Session expired OR manually invalidated.
        #
        # POSSIBLE REASONS:
        # - Normal expiration
        # - Manual logout
        # - Password changed
        # - Admin revoked session
        #
        # SECURITY LEVEL:
        # LOW to MEDIUM
        #
        # ACTION:
        # - No extra revocation needed
        # - Cleanup expired sessions optionally
        #
        # USER NOTIFICATION?
        # NO
        #
        # RECOMMENDATION:
        # Expired sessions can be cleaned with cron/background job.
        # ------------------------------------------------------------
        if session.expiresAt < now or not session.isValid:
            print("Session expired OR manually invalidated.")
            raise AppException(
                status_code=401,
                message="Token invalid or already Expired",
                error="INVALID_TOKEN"
         )


        # ------------------------------------------------------------
        # CASE:
        # Browser fingerprint mismatch.
        #
        # POSSIBLE REASONS:
        # - Token theft
        # - Browser/environment changed
        # - Fingerprint drift
        #
        # SECURITY LEVEL:
        # HIGH
        #
        # ACTION:
        # - Revoke CURRENT SESSION
        # - Log suspicious activity
        #
        # USER NOTIFICATION?
        # YES — recommended if mismatch confidence is high.
        #
        # RECOMMENDATION:
        # Fingerprints should NOT be overly strict because
        # browsers/extensions/update changes can alter them.
        # ------------------------------------------------------------
        if not persistent_device_id and session.fingerprint != current_fingerprint:
            print("Browser fingerprint mismatch.")
            raise AppException(
                status_code=401,
                message="Token invalid or already Expired",
                error="INVALID_TOKEN"
            )
    
        refresh_token_payload = {
            "userId": str(session.userId)
        }

        new_refresh_token = create_refresh_token(refresh_token_payload)

        access_token_payload = {
            "userId": str(session.userId),
            "sessionId": str(session.id)
        }

        access_token = create_access_token(access_token_payload)

        session.lastActiveAt = now
        session.refreshToken = new_refresh_token

        await db.commit()

        await asyncio.gather(
            self.redis_service.del_by_prefix(cache_key),
            self.redis_service.del_by_prefix(cache_key_user_list),
            self.redis_service.del_by_prefix(cache_key__list)
        )

        return {
            "access_token": access_token,
            "refresh_token": new_refresh_token,
        }
        
    async def revoke_session(self,req, res, sessionId, db):
        user_id = req.state.userId
        session_id = req.state.sessionId
        now = datetime.now(UTC)
        cache_key_list = SessionCacheKeys.sessions_list(None, is_prefix=True)
        cache_key = SessionCacheKeys.single_session(sessionId)
        user_cache_key_list = SessionCacheKeys.user_sessions(user_id, None, is_prefix=True)

        session = await self.sessionRepo.get_session_by_id(db, sessionId)
        
        if not session:
            raise AppException(status_code=404, message="Session Not Found", error="NOT_FOUND")
        
        if not session.isValid:
            raise AppException(status_code=400, message="Session is Already invalid", error="BAD_REQUEST")
        if session.userId != user_id:
            raise AppException(status_code=403, message="You are not allowed to revoke this session", error="NOT_ALLOWED")
        session.revokeAt = now
        session.revokeReason = "Manual Session Revokation."
        session.isValid = False
        await db.commit()
        await asyncio.gather(
            self.redis_service.del_by_prefix(cache_key_list),
            self.redis_service.del_by_prefix(user_cache_key_list),
            self.redis_service.del_key(cache_key)
        )
        return session
        
        
        

    
     
            

        
        
        
