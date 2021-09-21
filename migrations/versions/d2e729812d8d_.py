"""empty message

Revision ID: d2e729812d8d
Revises: 
Create Date: 2021-10-04 15:08:56.211313

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd2e729812d8d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('offices',
    sa.Column('usa_state', sa.String(length=10), nullable=True),
    sa.Column('office_code', sa.String(length=10), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('office_code')
    )
    op.create_table('users',
    sa.Column('username', sa.String(length=10), nullable=False),
    sa.Column('password', sa.String(length=100), nullable=True),
    sa.Column('can_update_status_for', sa.String(length=10), nullable=True),
    sa.Column('can_update_password_for', sa.String(length=10), nullable=True),
    sa.Column('can_create_update_delete_orders', sa.String(length=1), nullable=True),
    sa.Column('is_admin', sa.String(length=1), nullable=True),
    sa.PrimaryKeyConstraint('username')
    )
    op.create_table('orders',
    sa.Column('order_number', sa.Integer(), nullable=False),
    sa.Column('uuid', sa.String(length=40), nullable=False),
    sa.Column('usa_state', sa.String(length=10), nullable=True),
    sa.Column('office_code', sa.String(length=10), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['office_code'], ['offices.office_code'], ),
    sa.PrimaryKeyConstraint('order_number')
    )
    op.create_index(op.f('ix_orders_uuid'), 'orders', ['uuid'], unique=True)
    op.create_table('status',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('office_code', sa.String(length=10), nullable=True),
    sa.Column('sequence_num', sa.Integer(), nullable=True),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['office_code'], ['offices.office_code'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('status')
    op.drop_index(op.f('ix_orders_uuid'), table_name='orders')
    op.drop_table('orders')
    op.drop_table('users')
    op.drop_table('offices')
    # ### end Alembic commands ###
