'''
Методы API приложения для работы с .csv файлами:
загрузка.
'''
from fastapi import APIRouter, UploadFile, File, Depends
from app.services.file_services import FileService
from app.models.files_models import (UploadResponse,
                                     SortedData)
router = APIRouter(
    prefix="/file",
    tags=["Files API"]
)


@router.post('/upload/', response_model=UploadResponse)
def upload(
        file: UploadFile = File(...),
        service: FileService = Depends()
) -> UploadResponse:
    '''Метод API для загрузки .csv файла.
    Args:
        file: UploadFile,
            объект, который предоставляет файл, может быть .csv или .tiff
        service: FileService,
            объект сервис
    Returns:
        UploadResponse объект, содержащий запрошенные данные'''
    return service.upload(file)


@router.get('/sorted-data/', response_model=SortedData)
def get_sorted_data(
        filename: str,
        service: FileService = Depends()
) -> SortedData:
    '''API-метод для распаковки .csv файла по его имени.
    Распаковка означает, что запрошенный файл будет прочитан
    и отсортированные массивы максимальных значений по строкам и столбцам
    будут возвращены с соответствующими индексами.
    Args:
        filename: str, имя .csv файла
        service: FileService, объект сервис
    Returns:
        SortedData объект, содержащий запрошенные данные'''
    return service.get_sorted_data(filename)


@router.delete('/delete/', response_model=None)
def delete_file(
    filename: str,
    service: FileService = Depends()
) -> None:
    '''Метод API для удаления загруженного .csv файла
    Args:
        filename: str, имя .csv файла
    Returns:
        None'''
    service.delete_file(filename)
