from fastapi import FastAPI, Depends
from fastapi_pagination import add_pagination

from core.config import ProjectConfig, get_configuration
from core.database import session, get_db

import users.routers as user_routers
import users.exceptions as user_exceptions

app = FastAPI()

@app.get('/')
def index():
    return {
        'message': 'Welcome to Fast API'
    }

@app.get('/settings')
def settings(settings: ProjectConfig = Depends(get_configuration)):
    ProjectConfig()
    return settings

app.include_router(user_routers.auth_router)
app.include_router(user_routers.user_router)

add_pagination(app)
