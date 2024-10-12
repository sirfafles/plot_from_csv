'''Модуль для управления кэшем приложения'''
import os
import shutil
from typing import IO, Any
import numpy as np
import numpy.typing as npt
from PIL import Image, UnidentifiedImageError
from app.settings import settings


def save_csv_as_npy(
    file: IO[Any],
    filename: str
) -> None:
    '''Процедура сохранения csv-файла в npy-файл
    Args:
        file: IO[Any],
            файловый объект
        filename: str,
            имя файла
    Returns:
        None'''
    try:
        csv_data = np.loadtxt(file,
                              delimiter=';',
                              dtype=np.float32)
    except Exception as exc:
        raise ValueError("Couldn't read .csv file") from exc
    cache = settings.cache
    path_to_npy = cache + filename+'.npy'
    np.save(path_to_npy, csv_data)


def save_tiff_as_npy(
    file: IO[Any],
    filename: str
) -> None:
    '''Процедура сохранения файла .tiff в формате .csv
    Args:
        file: IO[Any],
            файловый объект
        filename: str,
            имя файла
    Returns:
        None'''
    cache = settings.cache
    path_to_tiff = cache + filename + '.tiff'
    path_to_npy = cache + filename + '.npy'
    try:
        with open(path_to_tiff, "wb+") as buffer:
            shutil.copyfileobj(file, buffer)
        image = Image.open(path_to_tiff)
        np.save(path_to_npy, image)
        os.remove(path_to_tiff)
    except Exception as exc:
        raise UnidentifiedImageError("Couldn't read .tiff file") from exc


def load_npy(
    filename: str
) -> npt.NDArray[Any]:
    '''Процедура загрузки данных из .npy файла
    Args:
        filename: str,
            filename string
    Returns:
        numpy.ndarray'''
    cache = settings.cache
    try:
        csv_data: npt.NDArray[Any] = np.load(cache+filename)
    except FileNotFoundError as exc:
        raise exc
    return csv_data


def clear_cache_start() -> None:
    '''Процедура удаления кэша после запуска сервера'''
    storage = settings.cache
    filenames = os.listdir(storage)
    for filename in filenames:
        file_path = storage + filename
        os.remove(file_path)
    print("CacheManagement: All temporary files were removed after starting.")


def clear_cache_file(filepath: str) -> None:
    '''Процедура удаляет кэш файл
    Args:
        filename: str,
            имя файла
    Returns:
        None'''
    try:
        os.remove(filepath)
    except FileNotFoundError as exc:
        raise exc
    print(f"CacheManagement: File {filepath} deleted.")
