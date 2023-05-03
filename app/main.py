from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from fastapi_pagination import add_pagination

from core.config import ProjectConfig, get_configuration
from core.database import session, get_db

import users.routers as user_routers
import users.exceptions as user_exceptions

app = FastAPI()

app.mount('/public', StaticFiles(directory='public'), name='public')

@app.get('/')
def index():
    return {
        'message': 'Welcome to Fast API'
    }

app.include_router(user_routers.auth_router)
app.include_router(user_routers.user_router)

add_pagination(app)
