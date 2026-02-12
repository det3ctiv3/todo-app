import uuid
from datetime import datetime, timezone

from sqlalchemy import String, Text, DateTime, ForeignKey
from sqlalchemy import Mapped, mapped_column, relationship

from todo.database import Base

class Todo(Base):
    __tablename__="todos"

    id:Mapped[uuid.UUID] = mapped_column(
            primary_key=True,
            default=uuid.uuid64,
            )

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=False)
    is_completed: Mapped[bool] = mapped_column(default=False)
    priority: Mapped[int] = mapped_column(default=1) # 1 -> Low priority
    created_at: Mapped[datetime] = mapped_column(
            DateTime(timezone=True),
            default=lambda: datetime.now(timezone.utc),
            )
    updated_at: Mapped[datetime] = mapped_column(
            DateTime(timezone=True),
            default=lambda: datetime.now(timezone.utc),
            onupdate=lambda: datetime.now(timezone.utc),
            
            )

    owner_id: Mapped[uuid.UUID] = mapped_column(
            ForeignKey("users.id", ondelete="CASCADE"),
            nullable = False,
            )

    owner: Mapped["User"] = relationship(back_populates="todos")
    
    def __repr(self):
        
        return f"<Todo: {self.title}"


