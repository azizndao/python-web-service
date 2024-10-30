from fastapi import APIRouter, Depends, HTTPException
from typing import List
from contextlib import closing
from ..database import get_db
from ..schemas import Task, TaskCreate
from ..security import get_current_user

router = APIRouter()

@router.post("/tasks/", response_model=Task)
async def create_task(task: TaskCreate, current_user: dict = Depends(get_current_user)):
    with closing(get_db()) as conn:
        with closing(conn.cursor()) as c:
            c.execute(
                "INSERT INTO tasks (user_id, title, description, due_date) VALUES (?, ?, ?, ?)",
                (current_user["id"], task.title, task.description, task.due_date)
            )
            conn.commit()
            
            last_id = c.lastrowid
            c.execute("SELECT * FROM tasks WHERE id = ?", (last_id,))
            result = c.fetchone()
            
            return {
                "id": result[0],
                "user_id": result[1],
                "title": result[2],
                "description": result[3],
                "status": result[4],
                "due_date": result[5],
                "created_at": result[6]
            }

@router.get("/tasks/", response_model=List[Task])
async def get_user_tasks(current_user: dict = Depends(get_current_user)):
    with closing(get_db()) as conn:
        with closing(conn.cursor()) as c:
            c.execute("SELECT * FROM tasks WHERE user_id = ?", (current_user["id"],))
            results = c.fetchall()
            
            tasks = []
            for r in results:
                tasks.append({
                    "id": r[0],
                    "user_id": r[1],
                    "title": r[2],
                    "description": r[3],
                    "status": r[4],
                    "due_date": r[5],
                    "created_at": r[6]
                })
            return tasks

@router.put("/tasks/{task_id}")
async def update_task_status(task_id: int, status: str, current_user: dict = Depends(get_current_user)):
    with closing(get_db()) as conn:
        with closing(conn.cursor()) as c:
            c.execute("SELECT user_id FROM tasks WHERE id = ?", (task_id,))
            task = c.fetchone()
            if not task or task[0] != current_user["id"]:
                raise HTTPException(status_code=404, detail="Task not found")
            
            c.execute("UPDATE tasks SET status = ? WHERE id = ?", (status, task_id))
            conn.commit()
            return {"message": "Task updated successfully"}

@router.delete("/tasks/{task_id}")
async def delete_task(task_id: int, current_user: dict = Depends(get_current_user)):
    with closing(get_db()) as conn:
        with closing(conn.cursor()) as c:
            c.execute("SELECT user_id FROM tasks WHERE id = ?", (task_id,))
            task = c.fetchone()
            if not task or task[0] != current_user["id"]:
                raise HTTPException(status_code=404, detail="Task not found")
            
            c.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            conn.commit()
            return {"message": "Task deleted successfully"} 