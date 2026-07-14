from app.core.config import config
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

# change the echo to True to see the verbose version of the engine
engine = create_async_engine(config.db_url, echo=False)
Session = async_sessionmaker(bind=engine, expire_on_commit=False)
#Base contains metadata to create your tables
Base = declarative_base()

from .user import User, UserAuth, UserPost  # noqa: E402 (must come after Base is defined)

__all__ = [
    "User",
    "UserAuth",
    "UserPost",
]
