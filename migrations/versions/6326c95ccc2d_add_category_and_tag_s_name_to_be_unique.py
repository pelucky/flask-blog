"""add category and tag's name to be unique

Revision ID: 6326c95ccc2d
Revises: 0339c8491b87
Create Date: 2017-10-22 22:36:23.902000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6326c95ccc2d'
down_revision = '0339c8491b87'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'categories', ['name'])
    op.create_unique_constraint(None, 'tags', ['name'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'tags', type_='unique')
    op.drop_constraint(None, 'categories', type_='unique')
    # ### end Alembic commands ###
