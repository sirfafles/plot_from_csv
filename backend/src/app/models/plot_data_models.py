'''
Модели данных для построения графиков из .csv файлов
'''
from pydantic import BaseModel


class Plot2D(BaseModel):
    '''Модель данных, предоставляющая данные для двумерного графика'''
    x_range: list[float]
    x_data: list[float]


class Plot3D(BaseModel):
    '''Модель данных, предоставляющая данные для трехмерного графика'''
    z_data: list[list[float]]
    z_data_db: list[list[float]]


class RadiometricResolutionAz(BaseModel):
    '''Модель данных для радиометрического разрешения по азимуту'''
    x_range: list[float]
    x_data: list[float]
    az_freq: int
    speed: float
    resolution_val: float


class RadiometricResolutionRg(BaseModel):
    '''Модель данных для радиометрического разрешения по дальности'''
    x_range: list[float]
    x_data: list[float]
    range_freq: int
    resolution_val: float
