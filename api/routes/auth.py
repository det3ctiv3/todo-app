from typing import Annotated 

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.deps import get_db, get_current_user
from core.security import verify_password, create_access_token
from crud.user import create_user, get_user_by_email
from models.user import User 
from schemas.user import UserCreate, UserLogin, UserRead, Token 

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post(
    "/register",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
)

async def register(
    payload: UserCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    ):
    # Register a new account
    existing = await get_user_by_email(db, payload.email)
    if existing:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = "Email already registered",
        )

    user = await create_user(db, payload)
    return user 


@router.post("/login", response_model = Token)
async def login(
    payload: UserLogin,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    
    # Authenticate and return a JWT access Token
    user = await get_user_by_email(db, payload.email)
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Incorrect email or password",
        )

    token = create_access_token(subject = str(user.id))
    return Token(access_token = token)

@router.get("/me", response_model = UserRead)
async def read_current_user(
    current_user: Annotated[User, Depends(get_current_user)],
    ):

    # Return the currently authenticated user's profile
    return current_user
