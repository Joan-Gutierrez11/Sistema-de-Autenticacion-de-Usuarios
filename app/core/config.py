from pydantic import BaseSettings
from dotenv import find_dotenv

class ProjectConfig(BaseSettings):
    DB_HOST: str = 'localhost'
    DB_DATABASE_NAME: str = 'photography_posts_api'
    DB_USER: str
    DB_PASS: str
    DB_DRIVER: str
    DB_PORT:int = 3306 # MySQL Port default

    class Config:
        env_file = find_dotenv(filename='.env', usecwd=True)


__project_configuration = None

def get_configuration() -> ProjectConfig:
    '''
    Return a singleton instance of object that contains variables for configuration of the project
    '''

    global __project_configuration # Indicate that's variable is global in this module

    if not __project_configuration:
        __project_configuration = ProjectConfig()
    
    return __project_configuration