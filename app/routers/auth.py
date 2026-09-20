from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import get_db
from app.models import User
from app.schemas import UserCreate, Token
from app.security import hash_password, verify_password, create_token

router = APIRouter()

# Schema لاستقبال بيانات تسجيل الدخول
class UserLogin(BaseModel):
    email: str
    password: str

@router.post("/register")
def register(data: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    user = User(
        name=data.name, 
        email=data.email, 
        password_hash=hash_password(data.password), 
        role=data.role
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"id": user.id, "name": user.name, "email": user.email, "role": user.role}

@router.post("/login")
def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    # البحث عن المستخدم بالبريد الإلكتروني
    user = db.query(User).filter(User.email == user_credentials.email).first()
    
    # التحقق من وجود المستخدم وصحة كلمة السر
    if not user or not verify_password(user_credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="البريد الإلكتروني أو كلمة المرور غير صحيحة"
        )
    
    # إنشاء التوكين عند صحة البيانات
    access_token = create_token({"sub": user.email, "role": user.role})
    return {"access_token": access_token, "token_type": "bearer", "user": {"email": user.email, "role": user.role}}