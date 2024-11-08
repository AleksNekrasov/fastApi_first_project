from enum import Enum

#Enum  для пола:
class GenderEnum(str, Enum):
    MALE = "мужчина"
    FEMALE = "женщина"

#Enum для профессии
class ProfessionEnum(str, Enum):
    DEVELOPER = "разработчик"
    DESIGNER = "дизайнер"
    MANAGER = "менеджер"
    TEACHER = "учитель"
    DOCTOR = "врач"
    ENGINEER = "инженер"
    MARKETER = "маркетолог"
    WRITER = "писатель"
    ARTIST = "художник"
    LAWYER = "юрист"
    SCIENTIST = "ученый"
    NURSE = "медсестра"
    UNEMPLOYED = "безработный"

#опишем простую модель для постов
class StatusPost(str, Enum):
    PUBLISHED = "опубликован"
    DELETED = "удален"
    UNDER_MODERATION = "на модерации"
    DRAFT = "черновик"
    SCHEDULED = "отложенная публикация"

#Модель с комментариями
#В этой модели нам необходимо будет связать комментарий, как с автором комментария,
# так и с постом, к которому этот комментарий был оставлен.
#Кроме того, в качестве демонстрации давайте тут добавим колонку
# is_publish – булево значение в формате опубликован комментарий или нет.
class RatingEnum(int, Enum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10