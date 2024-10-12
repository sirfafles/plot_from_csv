"""
Файл пакета API
"""
from fastapi import APIRouter
from app.api import files_api
from app.api import (plot_api)

router = APIRouter()
router.include_router(files_api.router)
router.include_router(plot_api.router)
