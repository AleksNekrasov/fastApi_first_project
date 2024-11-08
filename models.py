from sqlalchemy import ForeignKey, String, text, JSON, TEXT
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship

from sql_enums import *
from database import Base
from sql_enums import RatingEnum


#модель (таблица) профиля пользователей
class Profile(Base):
    first_name: Mapped[str]
    last_name: Mapped[str | None]
    age: Mapped[int | None]
    gender: Mapped[GenderEnum]
    profession: Mapped[ProfessionEnum] = mapped_column(
        default=ProfessionEnum.DEVELOPER,
        server_default=text("'UNEMPLOYED'")
    )
    interests: Mapped[list[str] | None] = mapped_column(ARRAY(String))
    contacts: Mapped[dict | None] = mapped_column(JSON)

    # Внешний ключ на таблицу users
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)

    # Обратная связь один-к-одному с User
    # Описание зависимостей (relationship) Profile с User
    #Один-к-одному (One-to-One)
    user: Mapped["User"] = relationship(
        "User",               # с каким классом(таблицей) связываемся
        back_populates="profile",      # связь с классом(таблицей) User
        uselist=False                  # Ключевой параметр для связи один-к-одному
    )

# описываем модель (таблица)(класс) пользователей
class User(Base):
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    #profile_id: Mapped[int | None] = mapped_column(ForeignKey('profiles.id'))

    #Описание зависимостей (relationship) User с Profile
    #Один-к-одному (One-to-One)  с Profile
    profile: Mapped["Profile"] = relationship(
        "Profile",     # с каким классом(таблицей) связываемся
        back_populates="user",  # связь с классом(таблицей) Profile
        uselist=False,          # Ключевой параметр для связи один-к-одному
        lazy="joined"           # Автоматически подгружает profile при запросе user
    )

    #Связь между User и Post:
    #Связь Один-ко-Многим
    posts: Mapped[list["Post"]] = relationship(
        "Post",
        back_populates="user",
        cascade="all, delete-orphan" # Удаляет посты при удалении пользователя
    )

    #Связь между User и Comment
    #Один-ко-Многим
    comment: Mapped[list["Comment"]] = relationship(
        "Comment",
        back_populates="user",
        cascade="all, delete-orphan" # Удаляет комментарии при удалении пользователя
    )

# модель поста
class Post(Base):
    title: Mapped[str]
    #content: Mapped[Text]
    content: Mapped[str] = mapped_column(TEXT)
    main_photo_url: Mapped[str]
    photos_url: Mapped[list[str] | None] = mapped_column(ARRAY(String))
    status: Mapped[StatusPost] = mapped_column(
        default=StatusPost.PUBLISHED,
        server_default=text("'DRAFT'"),
        nullable=False
    )
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    # Связь между Post и User:
    # Связь Многие-к-Одному
    user: Mapped["User"] = relationship(
        "User",
        back_populates="posts"
    )

    #Связь между Post и Comment:
    # Связь Один-ко-Многим
    comments: Mapped[list["Comment"]] = relationship(
        "Comment",
        back_populates="post",
        cascade="all, delete-orphan"  # Удаляет комменты при удалении поста
    )



# сама модель комментов
class Comment(Base):
    #content: Mapped[Text]
    content: Mapped[str] = mapped_column(TEXT)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    post_id: Mapped[int] = mapped_column(ForeignKey('posts.id'))
    is_published: Mapped[bool] = mapped_column(
        default=True,
        server_default=text("'false'")
    )
    rating: Mapped[RatingEnum] = mapped_column(
        default=RatingEnum.FIVE,
        server_default=text("'SEVEN'")
    )

    # Связь между Comment и Post:
    # Связь Многие-к-Одному
    post: Mapped["Post"] = relationship(
        "Post",
        back_populates="comments"
    )

    # Связь между Comment и User:
    # Связь Многие-к-Одному
    user: Mapped["User"] = relationship(
        "User",
        back_populates="comment"
    )

