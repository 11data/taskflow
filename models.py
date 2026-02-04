"""
TaskFlow Database Models
"""
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid

Base = declarative_base()


class Task(Base):
    """Task model for project management"""
    __tablename__ = "tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    assignee = Column(String(50), nullable=False)  # mira/felix/werner/sophie/martin/jon
    status = Column(String(50), nullable=False, default="backlog")  # backlog/todo/in-progress/review/done
    priority = Column(String(20), nullable=False, default="medium")  # low/medium/high/urgent
    category = Column(String(50), nullable=False, default="dev")  # dev/finance/marketing/admin/client
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    due_date = Column(DateTime, nullable=True)
    created_by = Column(String(50), nullable=False)

    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        return {
            "id": str(self.id),
            "title": self.title,
            "description": self.description,
            "assignee": self.assignee,
            "status": self.status,
            "priority": self.priority,
            "category": self.category,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "created_by": self.created_by,
        }
