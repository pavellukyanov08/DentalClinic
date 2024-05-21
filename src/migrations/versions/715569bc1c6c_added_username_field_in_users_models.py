"""Added username field in users models

Revision ID: 715569bc1c6c
Revises: 5ed8899e5f32
Create Date: 2024-05-19 21:23:50.905264

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '715569bc1c6c'
down_revision = '5ed8899e5f32'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('username', sa.String(length=100), nullable=True))
        batch_op.create_unique_constraint(None, ['username'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_column('username')

    # ### end Alembic commands ###
