"""empty message

Revision ID: 1689503617d8
Revises: 
Create Date: 2021-11-09 06:23:22.235398

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1689503617d8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('offices',
    sa.Column('office_code', sa.String(length=10), nullable=False),
    sa.Column('usa_state', sa.String(length=10), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.PrimaryKeyConstraint('office_code')
    )
    op.create_table('status',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('status_federal_office_code', sa.String(length=10), nullable=True),
    sa.Column('sequence_num', sa.Integer(), nullable=True),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.ForeignKeyConstraint(['status_federal_office_code'], ['offices.office_code'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('username', sa.String(length=20), nullable=False),
    sa.Column('password', sa.String(length=100), nullable=True),
    sa.Column('office_code', sa.String(length=10), nullable=True),
    sa.Column('can_update_status_for', sa.String(length=20), nullable=True),
    sa.Column('can_update_password_for', sa.String(length=20), nullable=True),
    sa.Column('can_create_update_delete_orders', sa.String(length=1), nullable=True),
    sa.Column('is_admin', sa.String(length=1), nullable=True),
    sa.ForeignKeyConstraint(['office_code'], ['offices.office_code'], ),
    sa.PrimaryKeyConstraint('username')
    )
    op.create_table('orders',
    sa.Column('order_number', sa.Integer(), nullable=False),
    sa.Column('uuid', sa.String(length=40), nullable=False),
    sa.Column('usa_state', sa.String(length=10), nullable=True),
    sa.Column('order_status', sa.Integer(), nullable=True),
    sa.Column('home_office_code', sa.String(length=10), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.ForeignKeyConstraint(['home_office_code'], ['offices.office_code'], ),
    sa.ForeignKeyConstraint(['order_status'], ['status.id'], ),
    sa.PrimaryKeyConstraint('order_number')
    )
    op.create_index(op.f('ix_orders_uuid'), 'orders', ['uuid'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_orders_uuid'), table_name='orders')
    op.drop_table('orders')
    op.drop_table('users')
    op.drop_table('status')
    op.drop_table('offices')
    # ### end Alembic commands ###
