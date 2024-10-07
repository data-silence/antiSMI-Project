from sqlalchemy.orm import mapped_column, Mapped

from api.db import Base


class TgUser(Base):
    __tablename__ = "telegram_user"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    telegram_id: Mapped[int] = mapped_column(unique=True, index=True)
    username: Mapped[str]
