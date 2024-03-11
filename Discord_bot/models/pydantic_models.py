from pydantic import BaseModel

class SendMessageRequest(BaseModel):
    message: str
    channel_id: int

class ChannelCreationData(BaseModel):
    channel_name: str
    role_name: str
    username: str
