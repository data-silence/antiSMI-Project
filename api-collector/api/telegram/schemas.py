from pydantic import BaseModel


class STgUser(BaseModel):
    telegram_id: int
    username: str
