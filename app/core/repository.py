import abc
from typing import Any, Generic, TypeVar, List
from typing_extensions import Annotated

import sqlalchemy as sa

from sqlalchemy.orm import Session
from pydantic import BaseModel as BaseModelSchema

from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi_pagination import Params

from core.database import Base


T = TypeVar('T')

class RepositoryInterface(abc.ABC, Generic[T], metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get_by_id(self, id: Any) -> T: 
        """
        Get model object by id
        
        Params:
        :id by identify object
        
        Return:
        A [T] model object
        """
        ...

    @abc.abstractmethod
    def all(self) -> List[T]:
        """ Get all model objects of database """
        ...

    @abc.abstractmethod
    def create(self, obj: T) -> T:
        """ Create a new object and insert in database """
        ...

    @abc.abstractmethod
    def update(self, obj: dict, id: Any) -> T: ...

    @abc.abstractmethod
    def delete(self, id: Any) -> T: ...

class GenericBaseRepository(RepositoryInterface[T]):
    model: T = None

    def __init__(self, db: Session):
        self.db = db

    def get_values_attrs_update(self, obj: dict):
        return {  key: value for key, value in obj.items() if value }

    def get_by_id(self, id: Any):
        return self.db.query(self.model).get(id)

    def all(self):
        return self.db.query(self.model).all()

    def create(self, obj: T):
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def update(self, obj: dict, id: Any):
        attrs_to_update = self.get_values_attrs_update(obj)
        query = self.db.query(self.model).filter_by(id=id)
        
        if attrs_to_update:
            query.update(attrs_to_update)
            self.db.commit()

        obj_return = query.first()
        return obj_return

    def delete(self, id: Any):
        query = self.db.query(self.model).filter_by(id=id)
        obj = query.first()
        query.delete()
        return obj

    