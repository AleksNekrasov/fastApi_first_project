import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    # этот код создает объект конфигурации, который загружает
    # переменные окружения из файла .env,
    # расположенного в той же директории, что и текущий файл,
    # что позволяет легко изменять настройки без необходимости жестко
    # фиксировать их в коде.
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    )

    #мы описали метод, который позволит генерировать ссылку
    # для асинхронного подключения к базе данных PostgreSQL
    # через SQLAlchemy.
    def get_db_url(self):
        return (f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@"
                f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}")

settings = Settings()
print(settings.get_db_url())