import os
import shutil

from fastapi import File, UploadFile
from core.config import get_configuration

class LocalFileSystem:
    
    def __init__(self, directory: str, app_url: str):
        self.directory = directory
        self.app_url = app_url

    def _create_location(self, path: str):
        return os.path.join(self.directory, path)

    def _create_directory_of_files(self, folder: str = None):
        if not os.path.exists(f'{self.directory}/{folder}'):
            os.makedirs(f'{self.directory}/{folder}')

    def upload_file(self, path: str, name: str, file: UploadFile):
        ext = file.filename.split('.').pop()
        self._create_directory_of_files(path)

        path_of_file = f"{path}/{name}.{ext}"
        location = self._create_location(path_of_file)
        with open(location, "wb+") as file_obj:
            shutil.copyfileobj(file.file, file_obj)
        return path_of_file

    def get_url(self, path):
        if not path:
            raise Exception("Path not provided")
        if not os.path.exists(f'{self.directory}/{path}'):
            raise Exception("File not exists")

        return f'{self.app_url}/{self.directory}/{path}'


