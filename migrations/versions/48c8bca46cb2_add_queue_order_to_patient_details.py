"""Add queue_order to Patient_details

Revision ID: 48c8bca46cb2
Revises: ddd685514ad3
Create Date: 2024-08-21 17:06:33.212912

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '48c8bca46cb2'
down_revision = 'ddd685514ad3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('patient_details', schema=None) as batch_op:
        batch_op.add_column(sa.Column('queue_order', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('patient_details', schema=None) as batch_op:
        batch_op.drop_column('queue_order')

    # ### end Alembic commands ###
