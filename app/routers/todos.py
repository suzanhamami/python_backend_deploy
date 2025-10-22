from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_database
from app.crud import TodoCRUD
from app.schemas import TodoCreate, TodoUpdate, TodoResponse, TodoListResponse

router = APIRouter(prefix="/todos", tags=["todos"])

def get_todo_crud(database: Session = Depends(get_database)) -> TodoCRUD:
    return TodoCRUD(database)

@router.post("/", response_model=TodoResponse, status_code=201)
def create_todo(
    todo_data: TodoCreate,
    todo_crud: TodoCRUD = Depends(get_todo_crud)
):
    """Create a new todo item"""
    return todo_crud.create_todo(todo_data)

@router.get("/", response_model=TodoListResponse)
def get_todos(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(10, ge=1, le=100, description="Number of items per page"),
    search: Optional[str] = Query(None, description="Search in title and description"),
    is_completed: Optional[bool] = Query(None, description="Filter by completion status"),
    todo_crud: TodoCRUD = Depends(get_todo_crud)
):
    """Get all todo items with pagination and filtering"""
    skip = (page - 1) * size
    todos, total = todo_crud.get_todos(
        skip=skip, 
        limit=size, 
        search=search, 
        is_completed=is_completed
    )
    
    return TodoListResponse(
        todos=todos,
        total=total,
        page=page,
        size=size
    )

@router.get("/{todo_id}", response_model=TodoResponse)
def get_todo(
    todo_id: int,
    todo_crud: TodoCRUD = Depends(get_todo_crud)
):
    """Get a specific todo item by ID"""
    todo = todo_crud.get_todo_by_id(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@router.put("/{todo_id}", response_model=TodoResponse)
def update_todo(
    todo_id: int,
    todo_data: TodoUpdate,
    todo_crud: TodoCRUD = Depends(get_todo_crud)
):
    """Update a todo item"""
    todo = todo_crud.update_todo(todo_id, todo_data)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@router.patch("/{todo_id}/toggle", response_model=TodoResponse)
def toggle_todo_completion(
    todo_id: int,
    todo_crud: TodoCRUD = Depends(get_todo_crud)
):
    """Toggle the completion status of a todo item"""
    todo = todo_crud.toggle_todo_completion(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@router.delete("/{todo_id}", status_code=204)
def delete_todo(
    todo_id: int,
    todo_crud: TodoCRUD = Depends(get_todo_crud)
):
    """Delete a todo item"""
    success = todo_crud.delete_todo(todo_id)
    if not success:
        raise HTTPException(status_code=404, detail="Todo not found")
    return None
