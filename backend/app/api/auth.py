from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from app.services.db import get_db
from app.core.security import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

class RegisterIn(BaseModel):
    email: EmailStr
    password: str
    name: str | None = None

class LoginIn(BaseModel):
    email: EmailStr
    password: str

@router.post("/register")
def register(body: RegisterIn, db: Session = Depends(get_db)):
    # store in users table via raw SQL to avoid model mismatch
    from sqlalchemy import text
    existing = db.execute(text("SELECT id FROM users WHERE email=:e"), {"e": body.email}).first()
    if existing:
        raise HTTPException(400, "Email already registered")
    import uuid
    db.execute(text("INSERT INTO users (id,email,name,password_hash,is_active,created_at,updated_at) VALUES (:id,:e,:n,:p,true,now(),now())"),
               {"id": str(uuid.uuid4()), "e": body.email, "n": body.name, "p": hash_password(body.password)})
    db.commit()
    return {"message": "registered"}

@router.post("/login")
def login(body: LoginIn, db: Session = Depends(get_db)):
    from sqlalchemy import text
    row = db.execute(text("SELECT id,password_hash FROM users WHERE email=:e"), {"e": body.email}).first()
    if not row or not verify_password(body.password, row.password_hash):
        raise HTTPException(401, "Invalid credentials")
    token = create_access_token(str(row.id))
    return {"access_token": token, "token_type": "bearer"}

@router.post("/refresh")
def refresh(user_id: str = Depends(__import__("app.core.deps", fromlist=["get_current_user"]).get_current_user)):
    return {"access_token": create_access_token(user_id), "token_type": "bearer"}
