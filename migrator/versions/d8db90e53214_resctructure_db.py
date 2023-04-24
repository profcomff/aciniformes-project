"""Resctructure DB

Revision ID: d8db90e53214
Revises: 85489ec3d0d0
Create Date: 2023-04-20 13:53:44.522154

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'd8db90e53214'
down_revision = '85489ec3d0d0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('auth')
    op.drop_column('fetcher', 'modify_ts')
    op.drop_column('fetcher', 'metric_name')
    op.drop_column('fetcher', 'metrics')
    op.add_column('metric', sa.Column('name', sa.String(), nullable=False))
    op.add_column('metric', sa.Column('ok', sa.Boolean(), nullable=False))
    op.drop_column('metric', 'metrics')
    op.add_column('receiver', sa.Column('url', sa.String(), nullable=False))
    op.add_column('receiver', sa.Column('method', sa.Enum('POST', 'GET', name='method', native_enum=False), nullable=False))
    op.add_column('receiver', sa.Column('receiver_body', sa.JSON(), nullable=False))
    op.drop_column('receiver', 'modify_ts')
    op.drop_column('receiver', 'name')
    op.drop_column('receiver', 'chat_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('receiver', sa.Column('chat_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('receiver', sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.add_column('receiver', sa.Column('modify_ts', postgresql.TIMESTAMP(), autoincrement=False, nullable=False))
    op.drop_column('receiver', 'receiver_body')
    op.drop_column('receiver', 'method')
    op.drop_column('receiver', 'url')
    op.add_column('metric', sa.Column('metrics', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=False))
    op.drop_column('metric', 'ok')
    op.drop_column('metric', 'name')
    op.add_column('fetcher', sa.Column('metrics', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=False))
    op.add_column('fetcher', sa.Column('metric_name', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.add_column('fetcher', sa.Column('modify_ts', postgresql.TIMESTAMP(), autoincrement=False, nullable=False))
    op.create_table('auth',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('username', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('password', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='auth_pkey')
    )
    # ### end Alembic commands ###
