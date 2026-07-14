from app.entities.user import User, UserPost, UserAuth
from app.repositories.user_repository import Repository
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

class Service():

    def __init__(self, session : AsyncSession):
        self.session = session
        self.repo = Repository(self.session)

    async def create_user(self, username : str, email : str, password : str) -> User:
        user = User(username, email, password)
        await self.repo.insert_user(user)
        return user
    
    async def create_post(self, content : str, user : User) -> UserPost:
        post = UserPost(content, user)
        await self.repo.insert_user_post(post)
        return post

    async def set_user_password(self, password : str, user : User) -> bool:
        return await self.repo.update_user_password(user.id, password )

    async def delete_user(self, user_id : int) -> bool:
        return await self.repo.delete_user(user_id)
    
    async def delete_post(self, post_id : int) -> bool:
        return await self.repo.delete_user_post(post_id)
    
    async def search_user_by_id(self, user_id : int) ->Optional[User]:
        return await self.repo.select_user_by_id(user_id)
    
    async def search_user_by_email(self, email : str) ->Optional[UserAuth]:
        return await self.repo.select_user_by_email(email)

    async def search_post_by_id(self, post_id : int) ->Optional[UserPost]:
        return await self.repo.select_post_by_id(post_id)

    async def get_all_users(self)->List[User]:
        return await self.repo.select_all_users()

    async def update_user_code(self, user_id : int)-> Optional[str]:
        return await self.repo.update_user_code(user_id)
    
    async def get_all_user_posts(self, user_id : int)->List[UserPost]:
        return await self.repo.select_all_user_post(user_id)
    
    async def get_all_posts(self)->List[UserPost]:
        return await self.repo.select_all_posts()

