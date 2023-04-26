import sqlalchemy as sa

from security.psswd import check_password, get_hash_password
from core.database import Base as SQLBaseModel

class User(SQLBaseModel):
    __tablename__ = 'users'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    username = sa.Column(sa.String(50), unique=True)
    email = sa.Column(sa.String(255), unique=True)
    first_name = sa.Column(sa.String(100))
    last_name = sa.Column(sa.String(100))
    date_joined = sa.Column(sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.sql.expression.text('now()'))
    password = sa.Column(sa.String(255), nullable=False)
    profile_image = sa.Column(sa.String(2055), nullable=True)

    def verify_password(self, pswd):
        return check_password(pswd, self.password)
    
    def set_password(self, pswd):
        self.password = get_hash_password(pswd)

