from pydantic import BaseModel


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