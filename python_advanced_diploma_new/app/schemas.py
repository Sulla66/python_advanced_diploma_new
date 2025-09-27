from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# Базовые схемы
class UserBase(BaseModel):
    id: int
    name: str

class SuccessResponse(BaseModel):
    result: bool

# Схемы для аутентификации
class UserCreate(BaseModel):
    name: str
    api_key: str

# Схемы для пользователей
class UserProfile(BaseModel):
    id: int
    name: str
    followers: List[UserBase]
    following: List[UserBase]

class UserResponse(SuccessResponse):
    user: UserProfile

# Схемы для твитов
class TweetCreate(BaseModel):
    tweet_data: str
    tweet_media_ids: Optional[List[int]] = None

class TweetIdResponse(SuccessResponse):
    tweet_id: int

class Author(BaseModel):
    id: int
    name: str

class LikeUser(BaseModel):
    user_id: int
    name: str

class TweetResponse(BaseModel):
    id: int
    content: str
    attachments: List[str]
    author: Author
    likes: List[LikeUser]
    created_at: str

class TweetsFeedResponse(SuccessResponse):
    tweets: List[TweetResponse]

# Схемы для медиа
class MediaUploadResponse(SuccessResponse):
    media_id: int

# Схемы для ошибок (опционально, для документации)
class ErrorResponse(BaseModel):
    result: bool = False
    error_type: str
    error_message: str

# Дополнительные схемы для удобства
class FollowInfo(BaseModel):
    id: int
    name: str

class UserMeResponse(SuccessResponse):
    user: dict  # Для /api/users/me, так как структура сложная

# Если нужно, можно добавить более специфичные схемы
class UserFollowStats(BaseModel):
    id: int
    name: str
    followers_count: int
    following_count: int