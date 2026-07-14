from fastapi import APIRouter, Depends, HTTPException
from app.dto.user import *
from app.dto.auth import * 
from app.services.user_services import Service as UserService
from .deps import *
import jwt
from app.core.config import config
from datetime import timezone, timedelta, datetime
import logging
logger = logging.getLogger(__name__)

auth_router = APIRouter(prefix="/auth")

@auth_router.post("/login", response_model=TokenResponse)
async def get_user(request : UserAuthLoginRequest, service : UserService = Depends(get_user_service)):
    user = await service.search_user_by_email(request.email)
    if user and user.check_password(request.password):
        token = jwt.encode(
            {"sub": str(user.user_id), "exp": datetime.now(timezone.utc) + timedelta(minutes=30)},
            config.secret_key,
            algorithm="HS256",
        )
        return {"access_token": token, "token_type": "bearer"}

    raise HTTPException(status_code=401, detail="provided credentials does not match any user")

@auth_router.post("/register", response_model=UserResponse)
async def add_user(request : UserAuthRegisterRequest, service : UserService = Depends(get_user_service) ):
    return await service.create_user(request.username, request.email, request.password)

@auth_router.post("/forgot-password", status_code=200)
async def change_password(request : UserPasswordRequest, user_service : UserService = Depends(get_user_service)):
    user = await user_service.search_user_by_email(request.email)
    if user:
        code = await user_service.update_user_code(user.user_id)
        logger.info("password reset for %s: %s", request.email, code) 
    return {"message" : "if this email is registered, a reset code has been sent"}   

@auth_router.post("/change-password", response_model=UserResponse)
async def set_password(request : UserChangePassword, user_service : UserService = Depends(get_user_service)):
    user_auth = await user_service.search_user_by_email(request.email)
    if not user_auth:
        raise HTTPException(status_code=404, detail="user not found!")
    if user_auth.check_security_code(request.security_code):
        await user_service.set_user_password(request.new_password, user_auth.user)
        return await user_service.search_user_by_id(user_auth.user_id)
    raise HTTPException(status_code=401, detail="wrong code")