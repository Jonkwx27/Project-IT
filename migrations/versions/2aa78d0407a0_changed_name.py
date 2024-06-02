"""Changed name

Revision ID: 2aa78d0407a0
Revises: a450b8e339ad
Create Date: 2024-05-30 15:48:54.906845

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2aa78d0407a0'
down_revision = 'a450b8e339ad'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('report', schema=None) as batch_op:
        batch_op.add_column(sa.Column('reviewed', sa.Boolean(), nullable=True))
        batch_op.drop_column('approved')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('report', schema=None) as batch_op:
        batch_op.add_column(sa.Column('approved', sa.BOOLEAN(), nullable=True))
        batch_op.drop_column('reviewed')

    # ### end Alembic commands ###