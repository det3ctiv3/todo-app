import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.todo import Todo 
from schemas.todo import TodoCreate, TodoUpdate 

async def get_todos(
        db: AsyncSession,
        owner_id: uuid.UUID,
        skip: int = 0, 
        limit: int = 20,
        ) -> list[Todo]:
            stmt = (
                    select(Todo)
                    .where(Todo.owner_id == owner_id)
                    .order_by(Todo.created_at.desc())
                    .offset(skip)
                    .limit(limit)
                    )
            result = await db.execute(stmt)
            return list(result.scalars().all())

async def get_todo(
        db: AsyncSession, todo_id: uuid.UUID, owner_id: uuid.UUID
        ) -> Todo:
        todo = Todo(**payload.model_dump(), owner_id=owner_id)
        stmt = select(Todo).where(Todo.id == todo.id, Todo.owner_id == owner_id)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

async def create_todo(
        db: AsyncSession, payload: TodoCreate, owner_id: uuid.UUID  
        ) -> Todo:
        todo = Todo(**payload.model_dump(), owner_id =owner_id)
        db.add(todo)
        await db.commit()
        await db.refresh(todo)
        return todo

async def update_todo(
        db: AsyncSession, todo: Todo, payload: TodoUpdate
        ) -> Todo:
        update_data = payload.model_dump(exclude_unset = True)
        for field, value in update_data.items():
            setattr(todo, field, value)

        await db.commit()
        await db.refresh(todo)
        return todo


async def delete_todo(db: AsyncSession, todo: Todo) -> None:
        await db.delete(todo)
        await db.commit()
        
        
