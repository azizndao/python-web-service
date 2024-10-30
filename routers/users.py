from fastapi import APIRouter, HTTPException
from contextlib import closing
import sqlite3
from ..database import get_db
from ..schemas import User, UserCreate
from ..security import get_password_hash

router = APIRouter()

@router.post("/users/", response_model=User)
async def create_user(user: UserCreate):
    with closing(get_db()) as conn:
        with closing(conn.cursor()) as c:
            hashed_password = get_password_hash(user.password)
            try:
                c.execute(
                    "INSERT INTO users (username, hashed_password) VALUES (?, ?)",
                    (user.username, hashed_password)
                )
                conn.commit()
                
                c.execute("SELECT * FROM users WHERE username = ?", (user.username,))
                result = c.fetchone()
                return {
                    "id": result[0],
                    "username": result[1],
                    "created_at": result[3]
                }
            except sqlite3.IntegrityError:
                raise HTTPException(status_code=400, detail="Username already registered") 