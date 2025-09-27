from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models import User  # Новый импорт!

def get_user_by_api_key(api_key: str, db: Session):
    user = db.query(User).filter(User.api_key == api_key).first()
    if not user:
        raise HTTPException(
            status_code=401,
            detail={
                "result": False,
                "error_type": "AuthenticationError",
                "error_message": "Invalid API key"
            }
        )
    return user