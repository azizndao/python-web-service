import sqlite3
from contextlib import closing

def init_db():
    """
    Initialise la base de données et crée les tables nécessaires si elles n'existent pas.
    """
    with closing(sqlite3.connect('tasks.db')) as conn:
        with closing(conn.cursor()) as c:
            # Création de la table utilisateurs
            c.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    hashed_password TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            # Création de la table tâches
            c.execute('''
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT,
                    status TEXT DEFAULT 'pending',
                    due_date TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            conn.commit()

def get_db():
    """
    Crée une connexion à la base de données.
    À utiliser avec un context manager.
    """
    return sqlite3.connect('tasks.db') 