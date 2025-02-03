from pathlib import Path

from fastapi_storages import FileSystemStorage
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    POSTGRES_DB: str
    DATABASE_URL: str
    BOT_TOKEN: str
    ADMIN_IDS: list[int] = [125468792, 125698542, 752103733]
    SECRET_KEY: str
    BASE_DIR: Path = Path(__file__).resolve().parent
    STORAGE_AUDIOS: Path = BASE_DIR / 'media/audios'
    STORAGE_IMAGES: Path = BASE_DIR / 'media/images'
    STORAGE_ANIMATIONS: Path = BASE_DIR / 'media/animations'
    STORAGES: dict = {}

    model_config = SettingsConfigDict(env_file=BASE_DIR / '.env')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._ensure_directories_exist(
            self.STORAGE_AUDIOS,
            self.STORAGE_IMAGES,
            self.STORAGE_ANIMATIONS,
        )

        self.STORAGES['audio'] = FileSystemStorage(path=self.STORAGE_AUDIOS)
        self.STORAGES['image'] = FileSystemStorage(path=self.STORAGE_IMAGES)
        self.STORAGES['animation'] = FileSystemStorage(path=self.STORAGE_ANIMATIONS)

    @staticmethod
    def _ensure_directories_exist(*paths: Path):
        """Создаёт директории, если их не существует."""
        for path in paths:
            path.mkdir(parents=True, exist_ok=True)

    @property
    def db_url(self):
        return self.DATABASE_URL
        # return f'postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.POSTGRES_DB}'


config = Settings()
