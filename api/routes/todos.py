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
    


@router.post(
        "/",
        response_model=TodoRead,
        status_code=status.HTTP_201_CREATED,
        )

async def create(
        payload: TodoCreate,
        db: Annotated[AsyncSession, Depends(get_db)],
        current_user: Annotated[User, Depends(get_current_user)],
        ):

        # Create a new to-do item
        return await create_todo(db, payload, owner_id=current_user.id)

@router.get("/{todo_id}", response_model=TodoRead)
async def read(
        todo_id: uuid.UUID,
        db: Annotated[AsyncSession, Depends(get_db)],
        current_user: Annotated[User, Depends(get_current_user)],
        ):
        
        # Get a specific todo by ID
        todo = await get_todo(db, todo_id, owner_id=current_user.id)
        if not todo:
            raise HTTPException(status_code = 404, detail = "Item not found")
        return todo


@router.patch("/{todo_id}", response_model=TodoRead)
async def update(
        todo_id: uuid.UUID,
        payload: TodoUpdate,
        db: Annotated[AsyncSession, Depends(get_db)],
        current_user: Annotated[AsyncSession, Depends(get_current_user)],
        ):
        
        # Partially update a todo item
        todo = await get_todo(db, todo_id, owner_id = current_user.id)
        if not todo:
            raise HTTPException(status_code = 404, detail = "Todo not found")

        return await update_todo(db, todo, payload)


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(
        todo_id: uuid.UUID, 
        db: Annotated[AsyncSession, Depends(get_db)],
        current_user: Annotated[AsyncSession, Depends(get_current_user)],
        ):
        
        # Delete a todo item
        todo = await get_todo(db, todo_id, owner_id=current_user.id)
        if not todo:
            raise HTTPException(status_code=404, detail="Todo not found")
        await delete_todo(db, todo)
