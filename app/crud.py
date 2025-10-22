from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import List, Optional
from app.models import Todo
from app.schemas import TodoCreate, TodoUpdate

class TodoCRUD:
    def __init__(self, database: Session):
        self.database = database

    def create_todo(self, todo_data: TodoCreate) -> Todo:
        todo = Todo(
            title=todo_data.title,
            description=todo_data.description,
            is_completed=todo_data.is_completed
        )
        self.database.add(todo)
        self.database.commit()
        self.database.refresh(todo)
        return todo

    def get_todo_by_id(self, todo_id: int) -> Optional[Todo]:
        return self.database.query(Todo).filter(Todo.id == todo_id).first()

    def get_todos(
        self, 
        skip: int = 0, 
        limit: int = 100, 
        search: Optional[str] = None,
        is_completed: Optional[bool] = None
    ) -> tuple[List[Todo], int]:
        query = self.database.query(Todo)
        
        # Apply search filter
        if search:
            query = query.filter(
                or_(
                    Todo.title.ilike(f"%{search}%"),
                    Todo.description.ilike(f"%{search}%")
                )
            )
        
        # Apply completion status filter
        if is_completed is not None:
            query = query.filter(Todo.is_completed == is_completed)
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        todos = query.offset(skip).limit(limit).all()
        
        return todos, total

    def update_todo(self, todo_id: int, todo_data: TodoUpdate) -> Optional[Todo]:
        todo = self.get_todo_by_id(todo_id)
        if not todo:
            return None
        
        update_data = todo_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(todo, field, value)
        
        self.database.commit()
        self.database.refresh(todo)
        return todo

    def delete_todo(self, todo_id: int) -> bool:
        todo = self.get_todo_by_id(todo_id)
        if not todo:
            return False
        
        self.database.delete(todo)
        self.database.commit()
        return True

    def toggle_todo_completion(self, todo_id: int) -> Optional[Todo]:
        todo = self.get_todo_by_id(todo_id)
        if not todo:
            return None
        
        todo.is_completed = not todo.is_completed
        self.database.commit()
        self.database.refresh(todo)
        return todo
