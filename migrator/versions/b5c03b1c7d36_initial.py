"""initial

Revision ID: b5c03b1c7d36
Revises: 
Create Date: 2023-01-31 04:25:35.923513

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b5c03b1c7d36'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('fetcher',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('type', sa.Enum('GET', 'POST', 'PING', name='fetchertype', native_enum=False), nullable=False),
    sa.Column('address', sa.String(), nullable=False),
    sa.Column('fetch_data', sa.String(), nullable=False),
    sa.Column('metrics', sa.JSON(), nullable=False),
    sa.Column('metric_name', sa.String(), nullable=False),
    sa.Column('delay_ok', sa.Integer(), nullable=False),
    sa.Column('delay_fail', sa.Integer(), nullable=False),
    sa.Column('create_ts', sa.DateTime(), nullable=False),
    sa.Column('modify_ts', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('metric',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('metrics', sa.JSON(), nullable=False),
    sa.Column('create_ts', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('receiver',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('chat_id', sa.Integer(), nullable=False),
    sa.Column('create_ts', sa.DateTime(), nullable=False),
    sa.Column('modify_ts', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('alert',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('data', sa.JSON(), nullable=False),
    sa.Column('receiver', sa.Integer(), nullable=False),
    sa.Column('filter', sa.String(), nullable=False),
    sa.Column('create_ts', sa.DateTime(), nullable=True),
    sa.Column('modify_ts', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['receiver'], ['receiver.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('alert')
    op.drop_table('receiver')
    op.drop_table('metric')
    op.drop_table('fetcher')
    # ### end Alembic commands ###
