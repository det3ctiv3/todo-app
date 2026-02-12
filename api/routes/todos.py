import uuid 
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from todo.api.deps import get_db, get_current_user
from todo.crud.todo import create_todo, delete_todo, get_todo, get_todos, update_todo
from todo.models.user import User
from todo.schemas.todo import TodoCreate, TodoRead, TodoUpdate

router = APIRouter(prefix = "/todos", tags = ["Todos"])

@router.get("/", reponse_model=list[TodoRead])
async def list_todos(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    ):

    # List all todos for the current user with pagination
    return await get_todos(db, owner_id=current_user.id, skip = skip, limit = limit)


