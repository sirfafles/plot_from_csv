'''Модуль методов для работы с матрицами'''
from typing import Any
import numpy as np
import numpy.typing as npt


def to_decibels(
        data: npt.NDArray[Any]
) -> npt.NDArray[Any]:
    '''Метод для перевода строки значений в децибелы
    Args:
        data: numpy.ndarray,
            массив
    Returns:
        numpy.ndarray массив значений в децибелах'''
    data[data <= 0] = 1e-6
    max_value = np.max(data)
    decibels_data: npt.NDArray[Any] = 20 * np.log10(data/max_value,
                                                    dtype=np.float32)
    return decibels_data
