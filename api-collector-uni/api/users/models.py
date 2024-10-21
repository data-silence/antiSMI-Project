from sqlalchemy.orm import mapped_column, Mapped

from api.db import Base


# class Users(Base):
#     __tablename__ = 'users'  # Имя таблицы в базе данных
#
#     username: Mapped[int] = mapped_column(BigInteger, primary_key=True)  # bigint
#     user_id: Mapped[int] = mapped_column(nullable=False)  # integer
#     first_name: Mapped[str] = mapped_column()  # text
#     last_name: Mapped[str] = mapped_column()  # text
#     subscribe_date: Mapped[str] = mapped_column()  # text
#     email: Mapped[str] = mapped_column()  # text
#     hashed_password: Mapped[str] = mapped_column()  # text
#     nickname: Mapped[str] = mapped_column()  # text, может быть пустым

class Users(Base):
    __tablename__ = 'api_auth_user'

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str]
    hashed_password: Mapped[str]

    def __repr__(self):
        return f"<UserModel(username={self.user_id}, email={self.email})>"
