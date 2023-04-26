from sqlalchemy import create_engine, URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

from core.config import  get_configuration

url_connection = URL.create(
    database=get_configuration().DB_DATABASE_NAME,
    host=get_configuration().DB_HOST,
    password=get_configuration().DB_PASS,
    username=get_configuration().DB_USER,
    port=get_configuration().DB_PORT,
    drivername=get_configuration().DB_DRIVER
)

engine = create_engine(url_connection)

session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db() -> Session :
    '''
    This function return a new database session, the connection is closed when once time use
    '''
    db = session()
    try:
        yield db
    finally:
        db.close()