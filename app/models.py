from sqlalchemy import Column, String, Integer
from .database import Base


class SlackEvent(Base):
    __tablename__ = "slack_events"
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    type = Column(String, nullable=False)
    channel = Column(String, nullable=False)
    user = Column(String, nullable=False)
    text = Column(String, nullable=False)
    event_ts = Column(String, nullable=False)
