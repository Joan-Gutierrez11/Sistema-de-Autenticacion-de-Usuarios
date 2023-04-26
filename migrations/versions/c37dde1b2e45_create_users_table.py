"""create_users_table

Revision ID: c37dde1b2e45
Revises: 
Create Date: 2023-04-22 13:58:29.361012

"""
from alembic import op
import sqlalchemy as sa

import datetime


# revision identifiers, used by Alembic.
revision = 'c37dde1b2e45'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('username', sa.String(50), unique=True, nullable=False),
        sa.Column('email', sa.String(255), unique=True, nullable=False),
        sa.Column('first_name', sa.String(100)),
        sa.Column('last_name', sa.String(100)),
        sa.Column('date_joined', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.sql.expression.text('now()'))
    )

def downgrade() -> None:
    op.drop_table('users')
