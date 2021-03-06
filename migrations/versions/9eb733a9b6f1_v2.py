"""v2

Revision ID: 9eb733a9b6f1
Revises: 2660edb81c24
Create Date: 2022-02-19 21:30:35.309043

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '9eb733a9b6f1'
down_revision = '2660edb81c24'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'password')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('password', mysql.VARCHAR(length=128), nullable=False))
    # ### end Alembic commands ###
