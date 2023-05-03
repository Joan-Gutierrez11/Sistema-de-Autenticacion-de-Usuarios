from fastapi_pagination import Params
from fastapi_pagination.ext.sqlalchemy import paginate

from core.repository import GenericBaseRepository
from users.models import User

class UserRepository(GenericBaseRepository[User]):
    model: User = User

    def paginate_all_users(self, params: Params):
        query = self.db.query(self.model)
        return paginate(query, params)

    def update_user_password_by_id(self, id: int, new_password: str) -> User:
        user:User = self.db.query(self.model).get(id)
        user.set_password(new_password)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_verified_user(self, username: str, password: str) -> User:
        user: User = self.db.query(self.model).filter_by(username=username).first()
        if not user or not user.verify_password(password):
            return None
        return user
