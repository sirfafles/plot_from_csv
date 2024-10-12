'''Сервисы для API по работе с .csv файлами'''
import uuid

import numpy as np
from fastapi import UploadFile

from app.settings import settings
from app.models.files_models import (UploadResponse,
                                     SortedData,
                                     FileType)
from app.cache import (clear_cache_file,
                       save_csv_as_npy,
                       save_tiff_as_npy,
                       load_npy)


class FileService:
    '''Класс сервис для работы с файлами'''

    def upload(
            self,
            file: UploadFile
    ) -> UploadResponse:
        '''Метод для загрузки файла. Файл может быть .csv или .tiff
    Все файлы будут загруены как .npy
    Args:
        file: UploadFile,
            объект предоставляющий файл
    Returns:
        UploadResponse объект хранящий запрашиваемые данные'''
        prefix = uuid.uuid4().hex
        name_by_upload = str(file.filename)
        splited_name = name_by_upload.split(sep='.')
        filename_no_type = ''.join(splited_name[0:-1])
        filename_human = filename_no_type+'.csv'
        filename = prefix + filename_no_type
        filetype = FileType(splited_name[-1])
        match filetype:
            case FileType.CSV:
                save_csv_as_npy(file.file, filename)
            case FileType.TIFF:
                save_tiff_as_npy(file.file, filename)
        response = UploadResponse(filename=filename+'.npy',
                                  filename_human=filename_human)
        return response

    def get_sorted_data(
            self,
            filename: str
    ) -> SortedData:
        '''Метод для распаковки .npy файла по его имени
        Распакова означает, что полученный файл будет прочитан
        и массивы будут рассортированы по максимальному
        значению в строках и столбцах
        и будут возвращены с соответсвующими индексами
        Args:
            filename: str, имя файла
        Returns:
            SortedData объект содержащий запрашиваемую информацию'''
        data = load_npy(filename)

        max_rg_val = np.amax(data, axis=1)
        max_az_val = np.amax(data, axis=0)

        rg_sorted_arg = max_rg_val.argsort()[::-1]
        az_sorted_arg = max_az_val.argsort()[::-1]

        max_rg_val = np.sort(max_rg_val)[::-1]
        max_az_val = np.sort(max_az_val)[::-1]

        response = SortedData(
            rg_max_values_sorted=max_rg_val.tolist(),
            rg_indexes_sorted=rg_sorted_arg.tolist(),
            az_max_values_sorted=max_az_val.tolist(),
            az_indexes_sorted=az_sorted_arg.tolist()
        )
        return response

    def delete_file(
            self,
            filename: str
    ) -> None:
        '''Метод для удаления загруженного .npy файла
        Args:
            filename: str, имя .npy файла
        Returns:
            None'''
        filepath = settings.cache+filename
        clear_cache_file(filepath)
