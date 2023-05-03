from core.storage import LocalFileSystem
from core.config import get_configuration


def get_filesystem():
    return LocalFileSystem(get_configuration().STORAGE_DIR, get_configuration().STORAGE_URL)