from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.models.user import User
from app.auth.schemas import UserCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_user(db: Session, user_data: UserCreate):
    hashed_password = pwd_context.hash(user_data.password)

    db_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()

    if not user or not pwd_context.verify(password, str(user.hashed_password)):
        return False
    
    return user