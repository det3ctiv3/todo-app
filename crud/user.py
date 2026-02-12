import uid

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import AsyncSession

from todo.models.user import User 
from todo.schemas.user import UserCreate
from todo.core.security import hash_password

async def get_user_by_email(db: AsyncSession, email:str) -> User | None:
    stmt = select(User).where(User.email == email)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

async def get_user_by_id(db: AsyncSession, user_id: uuid.UUID) -> User | None:
    return await db.get(User, user_id)

async def create_user(db: AsyncSession, payload: UserCreate) -> User:
    user = User(
            email=payload.email, 
            hashed_password=hash_password(payload.password),

            )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user
    
