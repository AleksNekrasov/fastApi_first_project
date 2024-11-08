"""update tables

Revision ID: ba925834c4c2
Revises: f0f0a2b7ab7c
Create Date: 2024-11-04 10:50:50.235027

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ba925834c4c2'
down_revision: Union[str, None] = 'f0f0a2b7ab7c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('profiles', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_unique_constraint(None, 'profiles', ['user_id'])
    op.create_foreign_key(None, 'profiles', 'users', ['user_id'], ['id'])
    op.drop_constraint('users_profile_id_fkey', 'users', type_='foreignkey')
    op.drop_column('users', 'profile_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('profile_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('users_profile_id_fkey', 'users', 'profiles', ['profile_id'], ['id'])
    op.drop_constraint(None, 'profiles', type_='foreignkey')
    op.drop_constraint(None, 'profiles', type_='unique')
    op.drop_column('profiles', 'user_id')
    # ### end Alembic commands ###
