from api.dao.base import BaseDao
from api.users.models import Users


class UserDAO(BaseDao):
    model = Users
