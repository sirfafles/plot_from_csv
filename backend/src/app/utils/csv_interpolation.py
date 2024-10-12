'''Модуль выполняет интерполяцию для строки значений'''
from typing import Any
import numpy as np
from scipy.interpolate import CubicSpline


def cubic_spline_interpolation(data: list[float],
                               coef: int) -> tuple[Any, Any]:
    '''Метод получения интерполяции строки
    Args:
        data: list,
            строка значений
        coef: float,
            коэффицент масштабирования
    Returns:
       список новых точек по оси x, список новых точек по по оси y'''
    data_len = len(data)
    data_len_interp = coef*data_len
    x_values_interp = np.linspace(0, data_len-1, data_len_interp-1).tolist()
    x_values = range(0, data_len)
    cubic_spline = CubicSpline(x_values, data)
    data_interp = cubic_spline(x_values_interp).tolist()
    return (x_values_interp, data_interp)
