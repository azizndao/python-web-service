from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from contextlib import closing
from ..database import get_db
from ..security import verify_password, create_access_token
from ..schemas import Token

router = APIRouter()

@router.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    with closing(get_db()) as conn:
        with closing(conn.cursor()) as c:
            c.execute("SELECT * FROM users WHERE username = ?", (form_data.username,))
            user = c.fetchone()
            if not user or not verify_password(form_data.password, user[2]):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Incorrect username or password",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            access_token = create_access_token(data={"sub": user[1]})
            return {"access_token": access_token, "token_type": "bearer"} 