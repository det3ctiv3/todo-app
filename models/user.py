import uuid
from datetime import datetime, timezone

from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[uuid.UUID] = mapped_column(
            primary_key=True,
            default=uuid.uuid4,
            )
    email: Mapped[str] = mapped_column(
            String(255),
            unique=True, 
            index=True,
            nullable=False,
            )

    hashed_password: Mapped[str] = mapped_column(
            String(255),
            nullable=False,
            )
    
    is_active:Mapped[bool] = mapped_column(default=True)
    created_at:Mapped[bool] = mapped_column(
            DateTime(timezone=True),
            default=lambda: datetime.now(timezone.utc),
            )

    todos: Mapped[list["Todo"]] = relationship(
            back_populates="owner",
            cascade="all, delete-orphan",
            lazy="selectin",
            ) 

    def __repr__(self) -> str:
        return f"<User {self.email}>"
    


