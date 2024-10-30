from fastapi import FastAPI
from .database import init_db
from .routers import auth, tasks, users

# Initialisation de l'application FastAPI
app = FastAPI(title="Task Management API")

# Initialisation de la base de données au démarrage
init_db()

# Inclusion des routers
app.include_router(auth.router, tags=["authentication"])
app.include_router(users.router, tags=["users"])
app.include_router(tasks.router, tags=["tasks"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 