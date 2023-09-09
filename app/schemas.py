from pydantic import BaseModel, EmailStr
from typing import Optional


class SlackEvent(BaseModel):
    """Slack event coming with Slack payload"""
    type: str
    channel: str
    user: str
    text: str
    event_ts: str


class SlackPayload(BaseModel):
    """Slack Payload with or without a challange or event"""
    token: str
    type: str
    challenge: str = None
    event: SlackEvent = None


class SlackPayloadOut(BaseModel):
    """Slack Payload Response with or without a challange or event"""
    challenge: str = None


class UserOut(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None
