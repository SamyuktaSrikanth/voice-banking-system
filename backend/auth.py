import bcrypt
from sqlalchemy.orm import Session
from models import User

def hash_password(password: str):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password: str, hashed: str):
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def authenticate_user(db: Session, customer_id: str, password: str):
    user = db.query(User).filter(User.customer_id == customer_id).first()

    if not user:
        return None

    if not verify_password(password, user.password_hash):
        return None

    return user