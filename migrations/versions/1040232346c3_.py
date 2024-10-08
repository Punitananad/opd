"""empty message

Revision ID: 1040232346c3
Revises: 84f64b60ed9d
Create Date: 2024-08-21 22:27:02.558033

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1040232346c3'
down_revision = '84f64b60ed9d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('opd_list', schema=None) as batch_op:
        batch_op.add_column(sa.Column('patient_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'patient_details', ['patient_id'], ['id'])

    with op.batch_alter_table('patient_details', schema=None) as batch_op:
        batch_op.add_column(sa.Column('can_view_records', sa.Boolean(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('patient_details', schema=None) as batch_op:
        batch_op.drop_column('can_view_records')

    with op.batch_alter_table('opd_list', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('patient_id')

    # ### end Alembic commands ###
