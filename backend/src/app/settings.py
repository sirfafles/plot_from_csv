"""
Определения класса настроек
"""
from pathlib import Path
from pydantic import BaseSettings


class Settings(BaseSettings):
    """
    Этот класс предоставляет настройки приложения
    """

    server_host: str
    """IP-адрес хоста"""
    server_port: int
    """Порт приложения"""
    cache: str
    """Путь в кэш"""

    class Config:
        """Настройки окружения программы.
        """

        env_file = '.env'
        """Имя файла с переменными окружения"""
        env_file_encoding = 'utf-8'
        """кодировка env_file"""

        def __str__(self) -> str:
            return str({
                'class':             self.__class__.__name__,
                'env_file':          self.env_file,
                'env_file_encoding': self.env_file_encoding
            })

    def __str__(self) -> str:
        return str({
            'class':       self.__class__.__name__,
            'base class':  'pydantic.BaseSettings',
            'server host': self.server_host,
            'server port': self.server_port
        })


settings = Settings(
    _env_file=Path(__file__).parents[2].resolve()/".env",
    _env_file_encoding='utf-8'
)
