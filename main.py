"""
TaskFlow API - Project Management System
"""
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
import uuid

from database import get_db, init_db
from models import Task

app = FastAPI(title="TaskFlow API", version="1.0.0")

# CORS for dashboard access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for local development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic models for request/response
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    assignee: str
    status: str = "backlog"
    priority: str = "medium"
    category: str = "dev"
    due_date: Optional[datetime] = None
    created_by: str


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    assignee: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    category: Optional[str] = None
    due_date: Optional[datetime] = None


class TaskResponse(BaseModel):
    id: str
    title: str
    description: Optional[str]
    assignee: str
    status: str
    priority: str
    category: str
    created_at: datetime
    updated_at: datetime
    due_date: Optional[datetime]
    created_by: str

    class Config:
        from_attributes = True


# API Endpoints
@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    init_db()


@app.get("/")
async def root():
    """Health check"""
    return {"status": "ok", "service": "TaskFlow API", "version": "1.0.0"}


@app.get("/tasks", response_model=List[TaskResponse])
async def list_tasks(
    assignee: Optional[str] = None,
    status: Optional[str] = None,
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """List all tasks with optional filters"""
    query = db.query(Task)
    
    if assignee:
        query = query.filter(Task.assignee == assignee)
    if status:
        query = query.filter(Task.status == status)
    if category:
        query = query.filter(Task.category == category)
    
    tasks = query.order_by(Task.created_at.desc()).all()
    return [task.to_dict() for task in tasks]


@app.get("/tasks/{task_id}", response_model=TaskResponse)
async def get_task(task_id: str, db: Session = Depends(get_db)):
    """Get single task by ID"""
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task.to_dict()


@app.post("/tasks", response_model=TaskResponse, status_code=201)
async def create_task(task_data: TaskCreate, db: Session = Depends(get_db)):
    """Create new task"""
    task = Task(
        id=uuid.uuid4(),
        title=task_data.title,
        description=task_data.description,
        assignee=task_data.assignee,
        status=task_data.status,
        priority=task_data.priority,
        category=task_data.category,
        due_date=task_data.due_date,
        created_by=task_data.created_by,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task.to_dict()


@app.patch("/tasks/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: str,
    task_data: TaskUpdate,
    db: Session = Depends(get_db)
):
    """Update existing task"""
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Update only provided fields
    update_data = task_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(task, key, value)
    
    task.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(task)
    return task.to_dict()


@app.delete("/tasks/{task_id}", status_code=204)
async def delete_task(task_id: str, db: Session = Depends(get_db)):
    """Delete task"""
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db.delete(task)
    db.commit()
    return None


@app.get("/tasks/by-assignee/{assignee}", response_model=List[TaskResponse])
async def get_tasks_by_assignee(assignee: str, db: Session = Depends(get_db)):
    """Get all tasks for specific assignee"""
    tasks = db.query(Task).filter(Task.assignee == assignee).order_by(Task.created_at.desc()).all()
    return [task.to_dict() for task in tasks]


@app.get("/stats")
async def get_stats(db: Session = Depends(get_db)):
    """Get task statistics"""
    total = db.query(Task).count()
    by_status = {}
    by_assignee = {}
    
    for status in ["backlog", "todo", "in-progress", "review", "done"]:
        by_status[status] = db.query(Task).filter(Task.status == status).count()
    
    for assignee in ["mira", "felix", "werner", "sophie", "martin", "jon"]:
        by_assignee[assignee] = db.query(Task).filter(Task.assignee == assignee).count()
    
    return {
        "total": total,
        "by_status": by_status,
        "by_assignee": by_assignee,
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
