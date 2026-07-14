import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from . import Base
from datetime import datetime, timezone, timedelta
from typing import Optional
import bcrypt
import secrets

class User(Base):
    __tablename__ = "users"
    
    id : Mapped[int] = mapped_column(primary_key=True, unique=True)
    username : Mapped[str] = mapped_column(sa.String, unique=True)
    created_at : Mapped[datetime] = mapped_column(server_default=sa.func.now())
    updated : Mapped[datetime] = mapped_column(onupdate= sa.func.now(), server_default=sa.func.now())
    auth : Mapped["UserAuth"] = relationship(
        "UserAuth", uselist=False, back_populates="user", cascade="all, delete-orphan"
    )
    posts : Mapped[List["UserPost"]] = relationship(
        "UserPost", uselist=True, back_populates="user", cascade="all, delete-orphan"
    )

    # orm approach enable user to add methods
    def __init__(self, username : str, email : str, password: str):
        super().__init__()
        self.username = username
        self.auth = UserAuth(email=email)
        self.auth.set_password(password)

    @property
    def email(self) ->str:
        return self.auth.email

    def __repr__(self): 
        return f"<User(username={self.username}, email={self.auth.email}, posts={self.posts})"

class UserAuth(Base):
    __tablename__ = "user_auth"
    user_id : Mapped[int] = mapped_column(sa.Integer, sa.ForeignKey("users.id") ,primary_key=True, nullable=False)
    email : Mapped[str] = mapped_column(unique=True)
    password_hashed : Mapped[str]
    security_code : Mapped[Optional[str]] =  mapped_column(sa.String, nullable=True)
    security_code_expires_at : Mapped[Optional[datetime]] = mapped_column(sa.DateTime(timezone=True), nullable=True)
    user : Mapped["User"] = relationship(
        "User", uselist=False, back_populates="auth"
    )

    def __init__(self, email : str):
        self.email = email

    def set_password(self, password : str)-> None:
        # bcrypt generates a random salt per-password and embeds it in the hash
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        self.password_hashed = hashed.decode() # store as str in the db

    def check_password(self, password : str)-> bool:
        return bcrypt.checkpw(password.encode(), self.password_hashed.encode())

    def set_security_code(self) ->None:
        self.security_code = f"{secrets.randbelow(1_000_000):06d}"
        self.security_code_expires_at = datetime.now(timezone.utc) + timedelta(minutes=15)

    def check_security_code(self, code : str) ->bool:
        if self.security_code is None or self.security_code_expires_at is None:
            return False
        if datetime.now(timezone.utc) > self.security_code_expires_at:
            return False
        return code == self.security_code

    def __repr__(self):
        return f"<UserAuth>username={self.user_id}, email={self.email}" 
    
class UserPost(Base):
    __tablename__ = "user_post"

    id : Mapped[int] = mapped_column(primary_key=True, unique=True)
    created_at : Mapped[datetime] = mapped_column(server_default=sa.func.now())
    user_id: Mapped[int] = mapped_column(sa.Integer ,sa.ForeignKey("users.id"), nullable=False, index=True)
    content: Mapped[str]
    user : Mapped["User"] = relationship(
        "User", back_populates="posts"
    )

    def __init__(self, content : str, user : User):
        super().__init__()
        self.content = content
        self.user = user

    @property
    def username(self) -> str:
        return self.user.username

    def __repr__(self):
        return f"<UserPost>{self.content}"