"""empty message

Revision ID: 5cbe8e095f73
Revises:
Create Date: 2022-12-12 23:01:59.037964

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5cbe8e095f73'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('fetcher',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('type', sa.Enum('GET', 'POST', 'PING', name='fetchertype', native_enum=False, length=10), nullable=False),
        sa.Column('address', sa.String(), nullable=False),
        sa.Column('fetch_data', sa.String(), nullable=True),
        sa.Column('matrics', sa.JSON(), nullable=False),
        sa.Column('matric_name', sa.String(), nullable=False),
        sa.Column('delay_ok', sa.Integer(), nullable=False),
        sa.Column('delay_fail', sa.Integer(), nullable=False),
        sa.Column('create_ts', sa.DateTime(), nullable=True),
        sa.Column('modify_ts', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('metric',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('metrics', sa.JSON(), nullable=False),
        sa.Column('create_ts', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('reciever',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('chat_id', sa.Integer(), nullable=False),
        sa.Column('create_ts', sa.DateTime(), nullable=True),
        sa.Column('modify_ts', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('alert',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('data', sa.JSON(), nullable=False),
        sa.Column('reciever_id', sa.Integer(), nullable=False),
        sa.Column('filter', sa.String(), nullable=False),
        sa.Column('create_ts', sa.DateTime(), nullable=True),
        sa.Column('modify_ts', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['reciever'], ['reciever.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('alert')
    op.drop_table('reciever')
    op.drop_table('metric')
    op.drop_table('fetcher')
