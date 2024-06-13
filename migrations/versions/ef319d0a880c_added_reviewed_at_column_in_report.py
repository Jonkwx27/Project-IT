"""Added reviewed_at column in Report

Revision ID: ef319d0a880c
Revises: 21ede30c83ed
Create Date: 2024-06-10 15:11:14.088175

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ef319d0a880c'
down_revision = '21ede30c83ed'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('report', schema=None) as batch_op:
        batch_op.add_column(sa.Column('reviewed_at', sa.DateTime(timezone=True), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('report', schema=None) as batch_op:
        batch_op.drop_column('reviewed_at')

    # ### end Alembic commands ###
