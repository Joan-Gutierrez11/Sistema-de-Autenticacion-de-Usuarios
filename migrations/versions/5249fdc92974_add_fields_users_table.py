"""add_fields_users_table

Revision ID: 5249fdc92974
Revises: c37dde1b2e45
Create Date: 2023-04-24 09:10:26.945174

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5249fdc92974'
down_revision = 'c37dde1b2e45'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('users', sa.Column('password', sa.String(255), nullable=False),)
    op.add_column('users', sa.Column('profile_image', sa.String(2055), nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'password')
    op.drop_column('users', 'profile_image')
