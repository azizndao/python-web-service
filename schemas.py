from pydantic import BaseModel
from typing import Optional
import datetime

class UserBase(BaseModel):
    """Modèle de base pour les utilisateurs"""
    username: str

class UserCreate(UserBase):
    """Modèle pour la création d'un utilisateur"""
    password: str

class User(UserBase):
    """Modèle complet d'un utilisateur"""
    id: int
    created_at: datetime.datetime

    class Config:
        orm_mode = True

class TaskBase(BaseModel):
    """Modèle de base pour les tâches"""
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime.datetime] = None

class TaskCreate(TaskBase):
    """Modèle pour la création d'une tâche"""
    pass

class Task(TaskBase):
    """Modèle complet d'une tâche"""
    id: int
    user_id: int
    status: str
    created_at: datetime.datetime

    class Config:
        orm_mode = True

class Token(BaseModel):
    """Modèle pour le jeton d'authentification"""
    access_token: str
    token_type: str 