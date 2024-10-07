from api.dao.base import BaseDao
from api.telegram.models import TgUser
from api.db import asmi_async_session_maker

class TgUserDAO(BaseDao):
    model = TgUser
