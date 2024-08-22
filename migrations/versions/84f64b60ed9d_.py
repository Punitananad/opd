"""empty message

Revision ID: 84f64b60ed9d
Revises: 48c8bca46cb2
Create Date: 2024-08-21 22:19:22.231707

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '84f64b60ed9d'
down_revision = '48c8bca46cb2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('opd_list',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('can_view_records', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('patient_details', schema=None) as batch_op:
        batch_op.drop_column('queue_order')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('patient_details', schema=None) as batch_op:
        batch_op.add_column(sa.Column('queue_order', sa.INTEGER(), nullable=True))

    op.drop_table('opd_list')
    # ### end Alembic commands ###
