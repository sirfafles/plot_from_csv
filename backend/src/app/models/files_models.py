'''
Модели данных для работы с файлами
'''
from enum import Enum
from aenum import MultiValueEnum
from pydantic import BaseModel


class Direction(Enum):
    '''Класс, представляющий направление'''
    RANGE = 'range'
    AZIMUTH = 'azimuth'


class FileType(MultiValueEnum):
    '''Класс, представляющий тип загружаемого файла'''
    CSV = 'csv'
    TIFF = 'tiff', 'tif'


class CacheData(BaseModel):
    '''Класс, представляющий идентификаторы запрашиваемых данных:
        filename: имя .npy файла,
        index: индекс строки или столбца,
        deirection: определяет направление (азимут или дальность)'''
    filename: str
    index: int
    direction: Direction


class UploadResponse(BaseModel):
    '''Класс, представляющий ответ на запрос на загрузку'''
    filename: str
    filename_human: str


class SortedData(BaseModel):
    '''Класс, представляющий ответ на запрос распаковки'''
    rg_max_values_sorted: list[float]
    rg_indexes_sorted: list[float]
    az_max_values_sorted: list[float]
    az_indexes_sorted: list[float]

    class Config:
        arbitrary_types_allowed = True
