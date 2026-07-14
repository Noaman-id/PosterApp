from app.entities.user import User, UserPost, UserAuth
from app.entities import Base, engine
from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Optional

class Repository():

    def __init__(self, session : AsyncSession) -> None:
        self.session = session

    async def insert_user(self, user : User) -> bool:
        try:
            self.session.add(user)
            await self.session.commit()
            return True
        except SQLAlchemyError:
            await self.session.rollback()
            raise

    async def insert_user_post(self, post : UserPost) -> bool:
        try:
            self.session.add(post)
            await self.session.commit()
            return True
        except SQLAlchemyError:
            await self.session.rollback()
            raise

    async def delete_user_post(self, post_id : int) -> bool:
        try:
            post = await self.session.get(UserPost, post_id)
            if post:
                await self.session.delete(post)
                await self.session.commit()
            return True
        except SQLAlchemyError:
            await self.session.rollback()
            raise

    async def delete_user(self, user_id : int) -> bool:
        try:
            user = await self.session.get(User, user_id)
            if user:
                await self.session.delete(user)
                await self.session.commit()
            return True
        except SQLAlchemyError:
            await self.session.rollback()
            raise

    async def select_user_by_id(self, user_id : int) -> Optional[User]:
        try:
            user = await self.session.get(User, user_id, options=(joinedload(User.auth),))
            if user:
                return user
            return None
        except SQLAlchemyError:
            raise

    async def select_post_by_id(self, post_id : int) -> Optional[UserPost]:
        try:
            post = await self.session.get(UserPost, post_id, options=(joinedload(UserPost.user),))
            if post:
                return post
            return None
        except SQLAlchemyError:
            raise

    async def select_user_by_email(self, email : str)->Optional[UserAuth]:
        try:
            stmt = select(UserAuth).where(UserAuth.email == email).options(joinedload(UserAuth.user))
            result = await self.session.scalars(stmt)
            return result.first()
        except SQLAlchemyError:
            raise

    async def select_all_users(self) -> List[User]:
        try:
            stmt = select(User).options(joinedload(User.auth), selectinload(User.posts))
            result = await self.session.scalars(stmt)
            return list(result.all())
        except SQLAlchemyError:
            raise

    async def update_user_password(self, user_id : int, password : str)->bool:
        try:
            user = await self.session.get(User, user_id)
            if user:
                user.auth.set_password(password)
                user.auth.security_code = None
                user.auth.security_code_expires_at = None
                await self.session.commit()
                return True
            return False
        except SQLAlchemyError:
            await self.session.rollback()
            raise

    async def update_user_code(self,user_id : int) ->Optional[str]:
        try:
            user = await self.session.get(UserAuth, user_id)
            if user:
                user.set_security_code() 
                await self.session.commit()
                return user.security_code
            return None
        except SQLAlchemyError:
            await self.session.rollback()
            raise

    async def select_all_user_post(self, user_id: int)-> List[UserPost]:
        try:
            stmt = select(UserPost).where(UserPost.user_id == user_id).options(joinedload(UserPost.user))
            result = await self.session.scalars(stmt)
            return list(result.all())
        except SQLAlchemyError:
            raise

    async def select_all_posts(self)-> List[UserPost]:
        try:
            stmt = select(UserPost).options(joinedload(UserPost.user))
            result = await self.session.scalars(stmt)
            return list(result.all())
        except SQLAlchemyError:
            raise