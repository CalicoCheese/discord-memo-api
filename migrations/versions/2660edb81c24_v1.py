"""v1

Revision ID: 2660edb81c24
Revises: 
Create Date: 2022-02-15 04:49:51.959987

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2660edb81c24'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('notice',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('type', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('title', sa.String(length=40), nullable=False),
    sa.Column('text', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('discord_id', sa.String(length=20), nullable=False),
    sa.Column('is_admin', sa.Boolean(), nullable=False),
    sa.Column('creation_date', sa.DateTime(), nullable=False),
    sa.Column('tos_agree', sa.DateTime(), nullable=False),
    sa.Column('password', sa.String(length=128), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('discord_id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('memo',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('owner_id', sa.Integer(), nullable=True),
    sa.Column('edit', sa.DateTime(), nullable=False),
    sa.Column('text', sa.Text(), nullable=False),
    sa.Column('encrypted', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['owner_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('memo')
    op.drop_table('user')
    op.drop_table('notice')
    # ### end Alembic commands ###
