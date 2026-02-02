from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.users import User
from app.schemas.auth_schema import UserRegister,TokenResponse
from app.auth.securities import hash_password, verify_password
from app.auth.jwt import create_access_token

router = APIRouter(prefix="/auth",tags=["Authentication"])

@router.post("/register")
def register(data: UserRegister, db:Session = Depends(get_db)):
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user = User(
        name = data.name,
        email = data.email,
        password_hash = hash_password(data.password),
        role="USER"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "User registered Successfully"}


@router.post("/login",response_model=TokenResponse)
def login(
    data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email==data.username).first()

    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid Credentials")
    
    token = create_access_token(user.id,  user.role)
    return {"access_token": token}