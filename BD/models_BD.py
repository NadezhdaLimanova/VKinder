from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):

    pass


class USERS(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    id_vk_users: Mapped[int] = mapped_column(nullable=False, unique=True)
    sex: Mapped[str] = mapped_column(String(30))
    age: Mapped[int] = mapped_column(String(30))
    city: Mapped[str] = mapped_column(String(50))

    applicant: Mapped["APPLICANTS"] = relationship(back_populates="user")
    favorite: Mapped["FAVORITES"] = relationship(back_populates="user")

    def __str__(self):
        return f"{self.id}, {self.id_vk_users}? {self.sex}, {self.age}, {self.city}"


class APPLICANTS(Base):
    __tablename__ = 'applicants'

    id: Mapped[int] = mapped_column(primary_key=True)
    id_user: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    id_vk_applicant: Mapped[int] = mapped_column(nullable=False, unique=True)
    photo_1: Mapped[str]
    photo_2: Mapped[str]
    photo_3: Mapped[str]

    user: Mapped["USERS"] = relationship(back_populates="applicant")

    def __str__(self):
        return f"{self.id}, {self.id_user}, {self.id_vk_applicant}, {self.first_name}, {self.last_name}, " \
               f"{self.photo_1}, {self.photo_2}, {self.photo_3}"


class FAVORITES(Base):
    __tablename__ = 'favorites'

    id: Mapped[int] = mapped_column(primary_key=True)
    id_user: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    id_vk_favorite: Mapped[int] = mapped_column(nullable=False, unique=True)
    photo_1: Mapped[str]
    photo_2: Mapped[str]
    photo_3: Mapped[str]

    user: Mapped["USERS"] = relationship(back_populates="favorite")

    def __str__(self):
        return f"{self.id}, {self.id_user}, {self.id_vk_favorite}, {self.first_name}, {self.last_name}, " \
               f"{self.photo_1}, {self.photo_2}, {self.photo_3}"


def create_tables(engine):
    # Base.metadata.drop_all(engine)  # если необходимо удалить базу данных
    Base.metadata.create_all(engine)