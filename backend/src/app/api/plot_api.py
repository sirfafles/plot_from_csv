'''
Методы API приложения для построения графиков из .csv файлов:
чтение, интерполяция данных и т.д.
'''
from fastapi import APIRouter, Depends
from app.models.files_models import CacheData
from app.services.plot_services import PlotService
from app.models.plot_data_models import (Plot2D,
                                         Plot3D,
                                         RadiometricResolutionAz,
                                         RadiometricResolutionRg)
router = APIRouter(
    prefix="/plot",
    tags=['Plot API']
)


@router.get('/row/', response_model=Plot2D)
def get_row(
        npy_request: CacheData = Depends(),
        service: PlotService = Depends()
) -> Plot2D:
    '''Метод API для получения конкретной
    строки или столбца из файла с использованием
    сервис объекта.
    Args:
        npy_request: CacheData объекты, которые идентифицируют
            запрашиваемые данные, подлежащие обработке
        service: PlotService,
            объект сервис
    Returns:
        Plot2D объект, содержащий запрошенные данные'''

    return service.get_row(npy_request)


@router.get('/interpolation/', response_model=Plot2D)
def get_interpolation(
        npy_request: CacheData = Depends(),
        eval_coef: int = 32,
        service: PlotService = Depends()
) -> Plot2D:
    '''Метод API для получения интерполяции
    определенной строки или столбца из
    файла с использованием сервис объекта.
    Args:
        npy_request: CacheData объекты, которые идентифицируют
            запрашиваемые данные, подлежащие обработке
        eval_coef: int число, определяющее, сколько выборок
            будет в интерполированной строке по сравнению с исходной строкой
        service: PlotService,
            сервис объект
    Returns:
        Plot2D объект, содержащий запрошенные данные'''
    return service.get_interpolation(npy_request, eval_coef)


@router.get('/decibels/', response_model=Plot2D)
def get_decibels(
        npy_request: CacheData = Depends(),
        service: PlotService = Depends()
) -> Plot2D:
    '''Метод API для получения определенной строки или столбца
    преобразованный в децибелы из файла
    с использованием сервис объекта.
    Args:
        npy_request: CacheData объекты, которые идентифицируют
            запрашиваемые данные, подлежащие обработке
        service: PlotService,
            сервис объект
    Returns:
        Plot2D объект, содержащий запрошенные данные'''
    return service.get_decibels(npy_request)


@router.get('/decibels-interpolation/', response_model=Plot2D)
def get_decibels_interpolation(
        npy_request: CacheData = Depends(),
        eval_coef: int = 32,
        service: PlotService = Depends()
) -> Plot2D:
    '''API-метод для получения интерполяции конкретной
    строки или столбца, преобразованной в децибелы, из файла с использованием
    сервис объекта.
    Args:
        npy_request: CacheData объекты, которые идентифицируют
            запрашиваемые данные, подлежащие обработке
        eval_coef: int число, определяющее, сколько выборок
            будет в интерполированной строке по сравнению с исходной строкой
        service: PlotService,
            сервис объект
    Returns:
        Plot2D объект, содержащий запрошенные данные'''
    return service.get_decibels_interpolation(npy_request, eval_coef)


@router.get('/level-line/', response_model=Plot2D)
def get_level_line(
        npy_request: CacheData = Depends(),
        coeficient: float = 0.7,
        service: PlotService = Depends()
) -> Plot2D:
    '''Метод API для получения данных для построения линии уровня,
    ограниченной максимальным значением в определенной строке
    или столбце из файла с использованием сервис объекта.
    Args:
        npy_request: CacheData объекты, которые идентифицируют
            запрашиваемые данные, подлежащие обработке
        coeficient: float число, определяющее порог
            линии уровня:
                threshold=(амплитуда исходных данных)*coefficient
        service: PlotService,
            сервис объект
    Returns:
        Plot2D объект, содержащий запрошенные данные'''
    response, _ = service.get_level_line(npy_request, coeficient)
    return response


@router.get('/radiometric-resolution/',
            response_model=RadiometricResolutionAz | RadiometricResolutionRg)
def get_radiometric_resolution(
        npy_request: CacheData = Depends(),
        deltaf: int = 1250000000,
        speed: int = 50,
        prf: int = 2000,
        coefficient: float = 0.7,
        service: PlotService = Depends()
) -> RadiometricResolutionAz | RadiometricResolutionRg:
    '''Метод API для получения данных с радиометрическим разрешением
    и точек для их построения.
    Args:
        npy_request: CacheData объекты, которые идентифицируют
            запрашиваемые данные, подлежащие обработке
        deltaf: int,
            частота АЦП
        speed: int,
            скорость спутника
        prf: int,
            частота повторения импульсов
        coeficient: float число, определяющее пороговое значение:
            threshold=(амплитуда исходных данных)*coefficient
        service: PlotService,
            сервис объект
    Returns:
        RadiometricResolutionAz or RadiometricResolutionRg
        объект, содержащий запрошенные данные'''
    return service.get_radiometric_resolution(npy_request,
                                              deltaf,
                                              speed,
                                              prf,
                                              coefficient)


@router.get('/3d-plot/',
            response_model=Plot3D)
def get_3d_plot(
        filename: str,
        radius: int = 30,
        service: PlotService = Depends()
) -> Plot3D:
    '''Метод API для получения обрезанной матрицы точек
    для построения 3d-поверхности.
    Args:
        filename: str,
            имя файла
        radius: int,
            радиус области вокруг максимума
        service: PlotService,
            объект сервис
    Returns:
        Plot3D объект, содержащий запрошенные данные'''
    return service.get_3d_plot(filename, radius)
