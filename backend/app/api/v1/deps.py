from fastapi import Depends
from app.entities import Session
from app.services.user_services import Service as UserService

async def get_db_session():
    session = Session()
    try:
        yield session
    finally:
        await session.close()

def get_user_service(session = Depends(get_db_session)) -> UserService:
    return UserService(session=session)
