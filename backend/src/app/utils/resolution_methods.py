'''Модуль для нахождения области рядом с максимумом функции
где все элементы больше заданного порога'''
import numpy as np


def resolution_points(data_x: list[float],
                      data_y: list[float],
                      threshold: float) -> tuple[float, float]:
    '''Метод для нахождения координат точки для радиометрического разрежения
    Args:
        data_x: list,
            x координаты sinc
        data_y: list,
            y координаты sinc
        threshold: float,
            значение по y для которого нужно найти координату по x
    Returns:
        float границы области слева и справа'''
    peak_area = find_peak_area(data_y, threshold)
    left_index = peak_area[0]
    right_index = peak_area[-1]
    return (data_x[left_index], data_x[right_index])


def find_peak_area(data: list[float],
                   threshold: float) -> list[int]:
    '''Метод для поиска области рядом
    с максимумом заданых значений,
       где все элементы выше заданного порога
    Args:
        data: list[float],
            заданый список floats
        threshold: float
            значение порога
    Returns:
        список содержащий индексы области'''

    max_ = max(data)
    max_id = data.index(max_)
    data_array = np.array(data)
    above_thrashold, = np.where(data_array > threshold)
    above_thrashold_len = len(above_thrashold)
    peak_areas = [[above_thrashold[0]],]
    for i in range(0, above_thrashold_len-1):
        if above_thrashold[i] + 1 != above_thrashold[i+1]:
            peak_areas.append([])
        peak_areas[-1].append(above_thrashold[i+1])
    for area in peak_areas:
        if area.__contains__(max_id):
            result = area
            break
    return result
