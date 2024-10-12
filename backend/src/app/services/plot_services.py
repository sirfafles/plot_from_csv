'''Сервисы для API по построению графиков из .csv файлов'''
from scipy.constants import speed_of_light
from scipy.interpolate import CubicSpline
from scipy.optimize import fmin, minimize_scalar
import numpy as np

from app.models.files_models import (Direction,
                                     CacheData)
from app.models.plot_data_models import (Plot2D,
                                         Plot3D,
                                         RadiometricResolutionAz,
                                         RadiometricResolutionRg)
from app.utils.csv_interpolation import cubic_spline_interpolation
from app.utils.matrices_ops import to_decibels
from app.utils.resolution_methods import resolution_points
from app.cache import load_npy


ACCURACY = 1e-9


class PlotService:
    '''Класс сервис для построения графиков из .npy файлов '''

    def get_row(
            self,
            npy_request: CacheData
    ) -> Plot2D:
        '''Метод для получения конкретной
        строки или столбца из .npy файла
        Args:
            npy_request: CacheData объекты, которые идентифицируют
        запрашиваемые данные для обработки
        Returns:
            PlotData объект, содержащий запрошенные данные'''
        data = load_npy(npy_request.filename)

        if npy_request.direction == Direction.RANGE:
            x_range = list(range(0, len(data[npy_request.index])))
            x_data = data[npy_request.index].tolist()
        elif npy_request.direction == Direction.AZIMUTH:
            x_range = list(range(0, len(data[:, npy_request.index])))
            x_data = data[:, npy_request.index].tolist()

        return Plot2D(x_range=x_range,
                      x_data=x_data)

    def get_interpolation(
            self,
            npy_request: CacheData,
            eval_coef: int
    ) -> Plot2D:
        '''Метод получения интерполяции
        определенной строки или столбца из .npy файла
        Args:
            npy_request: CacheData объекты, которые идентифицируют
                запрашиваемые данные, подлежащие обработке
            eval_coef: int число, определяющее, сколько выборок
            будет в интерполированной строке по сравнению с исходной строкой
        Returns:
            Plot2D объект, содержащий запрошенные данные'''
        x_data = self.get_row(npy_request).x_data
        x_range, interpolation = cubic_spline_interpolation(x_data, eval_coef)
        return Plot2D(x_range=x_range,
                      x_data=interpolation)

    def get_decibels(
            self,
            npy_request: CacheData
    ) -> Plot2D:
        '''Метод для получения определенной строки или столбца
        преобразованого в децибелы из .npy файла
        Args:
            npy_request: CacheData объекты, которые идентифицируют
                запрашиваемые данные, подлежащие обработке
        Returns:
            Plot2D объект, содержащий запрошенные данные'''
        row_data = self.get_row(npy_request)
        x_data_array = np.array(row_data.x_data)
        x_data_decibels = to_decibels(x_data_array).tolist()
        return Plot2D(x_range=row_data.x_range,
                      x_data=x_data_decibels)

    def get_decibels_interpolation(
            self,
            npy_request: CacheData,
            eval_coef: int,
    ) -> Plot2D:
        '''Метод получения интерполяции строки, преобразованной в децибелы
        Args:
            npy_request: CacheData объекты, которые идентифицируют
                запрашиваемые данные, подлежащие обработке
            eval_coef: int число, определяющее, сколько выборок
            будет в интерполированной строке по сравнению с исходной строкой
        Returns:
            Plot2D объект, содержащий запрошенные данные'''
        x_data_decibels = self.get_decibels(npy_request).x_data
        x_range, interpolation = cubic_spline_interpolation(x_data_decibels,
                                                            eval_coef)
        return Plot2D(x_range=x_range,
                      x_data=interpolation)

    def get_level_line(
            self,
            npy_request: CacheData,
            coeficient: float,
    ) -> tuple[Plot2D, tuple[float, float]]:
        '''Метод для получения данных для построения
    линии уровня, ограниченной максимальным значением в
    определенной строке или столбце из .npy файла.
    Args:
        npy_request: CacheData объекты, которые идентифицируют
            запрашиваемые данные, подлежащие обработке
        coeficient: float число, определяющее порог
            линии уровня:
                threshold=(амплитуда исходных данных)*coefficient
    Returns:
        Plot2D объект, содержащий запрошенные данные'''
        row_data = self.get_row(npy_request)
        x_range = row_data.x_range
        values = row_data.x_data
        aprox_max_index = x_range[values.index(max(values))]
        interp_object = CubicSpline(x_range, values)

        def negative_interpolation_value(
                coor: float
        ) -> float:
            return -float(interp_object(coor))
        max_arg = fmin(negative_interpolation_value,
                       [aprox_max_index],
                       disp=False,
                       xtol=ACCURACY)[0]
        max_value = float(interp_object(max_arg))
        threshold = max_value*coeficient
        left_x_aprox, right_x_aprox = resolution_points(x_range,
                                                        values,
                                                        threshold)

        def threshold_value_diff(
                coor: float
        ) -> float:
            return abs(float(interp_object(coor)) - threshold)
        left_x = minimize_scalar(threshold_value_diff,
                                 bounds=(left_x_aprox-1, left_x_aprox),
                                 tol=ACCURACY).x
        right_x = minimize_scalar(threshold_value_diff,
                                  bounds=(right_x_aprox, right_x_aprox+1),
                                  tol=ACCURACY).x
        left_value = float(interp_object(left_x))
        return Plot2D(x_range=[x_range[0], x_range[-1]],
                      x_data=[left_value, left_value]), (left_x, right_x)

    def get_radiometric_resolution(
            self,
            npy_request: CacheData,
            range_freq: int,
            speed: int,
            prf: int,
            coeficient: float
    ) -> RadiometricResolutionAz | RadiometricResolutionRg:
        '''Метод для получения данных радиометрического разрешения
        и точки для их построения.
    Args:
        npy_request: CacheData бъекты, которые идентифицируют
            запрашиваемые данные, подлежащие обработке
        range_freq: int,
            частота АЦП
        speed: int,
            скорость спутника
        prf: int,
            частота повторения импульсов
        coeficient: число, определяющее пороговое значение:
            threshold=(amplitude of original data)*coefficient
    Returns:
        RadiometricResolutionAz or RadiometricResolutionRg
        объект, содержащий запрошенные данные'''
        level_line, points = self.get_level_line(npy_request, coeficient)
        left_x, right_x = points
        delta = right_x - left_x
        x_range = [left_x, right_x]
        response: RadiometricResolutionAz | RadiometricResolutionRg
        if npy_request.direction == Direction.RANGE:
            resolution = delta * speed_of_light / 2 / range_freq
            response = RadiometricResolutionRg(x_range=x_range,
                                               x_data=level_line.x_data,
                                               range_freq=range_freq,
                                               resolution_val=resolution)
        elif npy_request.direction == Direction.AZIMUTH:
            resolution = delta*speed/prf
            response = RadiometricResolutionAz(x_range=x_range,
                                               x_data=level_line.x_data,
                                               az_freq=prf,
                                               speed=speed,
                                               resolution_val=resolution)
        return response

    def get_3d_plot(
            self,
            filename: str,
            radius: int,
    ) -> Plot3D:
        '''Метод для получения обрезанной матрицы точек
        для построения трехмерной поверхности.
    Args:
        filename: str,
            имя .npy файла
        radius: int,
            радиус области вокруг максимума
    Returns:
        Plot3D объект, содержащий запрошенные данные'''
        npy_data = load_npy(filename)

        # Индексы максимума
        arg_max = np.unravel_index(np.argmax(npy_data, axis=None),
                                   npy_data.shape)
        # Границы области вокруг максимума
        left = np.min([radius, arg_max[0]])
        right = np.min([radius, npy_data.shape[0]-1-arg_max[0]])
        top = np.min([radius, arg_max[1]])
        bottom = np.min([radius, npy_data.shape[1]-1-arg_max[1]])
        # Кроп
        cropped = npy_data[arg_max[0] - left:arg_max[0] + right,
                           arg_max[1] - top:arg_max[1] + bottom]
        npy_data = cropped

        db_npy_data = to_decibels(npy_data)
        return Plot3D(
            z_data=npy_data.tolist(),
            z_data_db=db_npy_data.tolist())
