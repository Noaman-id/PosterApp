from fastapi import APIRouter, Depends, HTTPException
from app.dto.user import *
from app.dto.auth import *
from app.entities.user import User 
from app.services.user_services import Service as UserService
from .deps import *
from fastapi.security import OAuth2PasswordBearer
from app.core.config import config
import jwt
from typing import List, Optional

oauth2_schema = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(token : str = Depends(oauth2_schema),
                     service : UserService = Depends(get_user_service)) ->User:
    try:
        payload = jwt.decode(token, config.secret_key, algorithms=["HS256"])
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    user = await service.search_user_by_id(int(payload["sub"]))
    if user is None:
        raise HTTPException(status_code=401, detail="User no longer exists")
    return user

users_router = APIRouter(prefix="/users")

@users_router.get("/", response_model=list[UserResponse])
async def get_user(service : UserService = Depends(get_user_service), user : User = Depends(get_current_user)):
    return await service.get_all_users()
 
@users_router.get("/current", response_model=UserResponse)
def add_user(user : User = Depends(get_current_user) ):
    return user

@users_router.get("/get_my_posts", response_model=List[UserPostResponse])
async def get_my_posts(service : UserService = Depends(get_user_service) ,user : User = Depends(get_current_user)):
    return await service.get_all_user_posts(user.id)

@users_router.get("/get_posts", response_model=List[UserPostResponse])
async def getPosts(service : UserService = Depends(get_user_service) ,user : User = Depends(get_current_user)):
    return await service.get_all_posts()

@users_router.post("/post", response_model=UserPostResponse)
async def post(request : UserPostRequest ,service : UserService = Depends(get_user_service), user : User = Depends(get_current_user)):
    post = await service.create_post(request.content, user)
    return await service.search_post_by_id(post.id)

@users_router.get("/get_post/{post_id}", response_model=Optional[UserPostResponse])
async def get_post(post_id : int, service : UserService = Depends(get_user_service), user : User = Depends(get_current_user)):
    return await service.search_post_by_id(post_id=post_id)