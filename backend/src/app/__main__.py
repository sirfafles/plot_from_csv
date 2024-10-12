"""
Запуск приложения
"""
import uvicorn
from app.settings import settings
from app.cache import clear_cache_start

clear_cache_start()

uvicorn.run(
    "app.app:app",
    host=settings.server_host,
    port=settings.server_port,
    reload=True
)
