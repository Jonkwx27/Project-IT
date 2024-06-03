"""Added Notification table and added notified column in Report table

Revision ID: eb8f13e2da15
Revises: de3bbb8ecd96
Create Date: 2024-05-30 14:27:37.262130

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eb8f13e2da15'
down_revision = 'de3bbb8ecd96'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('notification',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('message', sa.String(length=255), nullable=False),
    sa.Column('timestamp', sa.DateTime(timezone=True), nullable=True),
    sa.Column('read', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('report', schema=None) as batch_op:
        batch_op.add_column(sa.Column('notified', sa.Boolean(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('report', schema=None) as batch_op:
        batch_op.drop_column('notified')

    op.drop_table('notification')
    # ### end Alembic commands ###
