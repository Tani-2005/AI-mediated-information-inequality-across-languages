"""Add task_session_id and task_id to post_task_measures for per-task workload tracking

Revision ID: 002_post_task_per_session
Revises: 001_initial_schema
Create Date: 2026-09-28 10:10:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '002_post_task_per_session'
down_revision: Union[str, None] = '001_initial_schema'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    naming_convention = {
        "uq": "uq_%(table_name)s_%(column_0_name)s",
    }
    with op.batch_alter_table('post_task_measures', schema=None, naming_convention=naming_convention) as batch_op:
        batch_op.add_column(sa.Column('task_session_id', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('task_id', sa.String(length=32), nullable=False))
        batch_op.create_foreign_key('fk_post_task_measures_task_session_id', 'task_sessions', ['task_session_id'], ['session_id'])
        batch_op.create_unique_constraint('uq_post_task_measures_task_session_id', ['task_session_id'])
        batch_op.drop_constraint('uq_post_task_measures_participant_id', type_='unique')

def downgrade() -> None:
    naming_convention = {
        "uq": "uq_%(table_name)s_%(column_0_name)s",
    }
    with op.batch_alter_table('post_task_measures', schema=None, naming_convention=naming_convention) as batch_op:
        batch_op.create_unique_constraint('uq_post_task_measures_participant_id', ['participant_id'])
        batch_op.drop_constraint('uq_post_task_measures_task_session_id', type_='unique')
        batch_op.drop_constraint('fk_post_task_measures_task_session_id', type_='foreignkey')
        batch_op.drop_column('task_id')
        batch_op.drop_column('task_session_id')
