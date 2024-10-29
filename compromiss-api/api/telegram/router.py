from fastapi import APIRouter

from api.exceptions import UserAlreadyExistsException
from api.telegram.dao import TgUserDAO
from api.telegram.schemas import STgUser
from datetime import datetime

router = APIRouter(
    prefix='/telegram',
    tags=['Telegram'],
)


@router.get('/register', response_model=STgUser)
async def register(telegram_id: int, username: str):
    existing_user = await TgUserDAO.get_one_or_none(telegram_id=telegram_id)
    if existing_user:
        raise UserAlreadyExistsException
    new_user = await TgUserDAO.add(telegram_id=telegram_id, username=username)
    return {"message": "User registered successfully", "user_id": new_user.telegram_id}
