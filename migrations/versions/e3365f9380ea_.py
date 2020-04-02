"""empty message

Revision ID: e3365f9380ea
Revises: 0d959eefdf7a
Create Date: 2020-04-02 17:11:59.929696

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e3365f9380ea'
down_revision = '0d959eefdf7a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('todolists',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('todos', sa.Column('todo_list', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'todos', 'todolists', ['todo_list'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'todos', type_='foreignkey')
    op.drop_column('todos', 'todo_list')
    op.drop_table('todolists')
    # ### end Alembic commands ###
