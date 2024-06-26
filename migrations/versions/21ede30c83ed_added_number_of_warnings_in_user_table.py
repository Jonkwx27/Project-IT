"""Added number_of_warnings in User table

Revision ID: 21ede30c83ed
Revises: c6bf95cb05d9
Create Date: 2024-05-30 23:36:08.222741

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '21ede30c83ed'
down_revision = 'c6bf95cb05d9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('number_of_warnings', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('number_of_warnings')

    # ### end Alembic commands ###
