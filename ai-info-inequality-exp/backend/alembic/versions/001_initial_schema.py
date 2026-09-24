"""Initial database schema migration

Revision ID: 001_initial_schema
Revises: 
Create Date: 2026-09-24 10:52:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '001_initial_schema'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.create_table('participants',
        sa.Column('participant_id', sa.String(length=64), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('status', sa.String(length=32), nullable=False),
        sa.Column('is_pilot', sa.Boolean(), nullable=False),
        sa.Column('ip_hash', sa.String(length=64), nullable=False),
        sa.PrimaryKeyConstraint('participant_id')
    )
    op.create_index(op.f('ix_participants_ip_hash'), 'participants', ['ip_hash'], unique=False)

def downgrade() -> None:
    op.drop_index(op.f('ix_participants_ip_hash'), table_name='participants')
    op.drop_table('participants')
