"""Init

Revision ID: febba504289a
Revises: 
Create Date: 2023-04-24 13:29:41.968973

"""
from alembic import op
import sqlalchemy as sa


revision = 'febba504289a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('alert',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('data', sa.JSON(), nullable=False),
    sa.Column('filter', sa.String(), nullable=False),
    sa.Column('create_ts', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('fetcher',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('type', sa.Enum('GET', 'POST', 'PING', name='fetchertype', native_enum=False), nullable=False),
    sa.Column('address', sa.String(), nullable=False),
    sa.Column('fetch_data', sa.String(), nullable=True),
    sa.Column('delay_ok', sa.Integer(), nullable=False),
    sa.Column('delay_fail', sa.Integer(), nullable=False),
    sa.Column('create_ts', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('metric',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('ok', sa.Boolean(), nullable=False),
    sa.Column('time_delta', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('receiver',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('url', sa.String(), nullable=False),
    sa.Column('method', sa.Enum('POST', 'GET', name='method', native_enum=False), nullable=False),
    sa.Column('receiver_body', sa.JSON(), nullable=False),
    sa.Column('create_ts', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('receiver')
    op.drop_table('metric')
    op.drop_table('fetcher')
    op.drop_table('alert')
