"""Initial database schema migration for all 12 entities

Revision ID: 001_initial_schema
Revises: 
Create Date: 2026-09-27 20:42:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '001_initial_schema'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # 1. participants
    op.create_table('participants',
        sa.Column('participant_id', sa.String(length=64), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('status', sa.String(length=32), nullable=False),
        sa.Column('is_pilot', sa.Boolean(), nullable=False),
        sa.Column('ip_hash', sa.String(length=64), nullable=False),
        sa.PrimaryKeyConstraint('participant_id')
    )
    op.create_index(op.f('ix_participants_ip_hash'), 'participants', ['ip_hash'], unique=False)

    # 2. consent_logs
    op.create_table('consent_logs',
        sa.Column('consent_id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('participant_id', sa.String(length=64), nullable=False),
        sa.Column('agreed_to_terms', sa.Boolean(), nullable=False),
        sa.Column('confirmed_age_residency', sa.Boolean(), nullable=False),
        sa.Column('consent_timestamp', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['participant_id'], ['participants.participant_id'], ),
        sa.PrimaryKeyConstraint('consent_id'),
        sa.UniqueConstraint('participant_id')
    )

    # 3. screening_logs
    op.create_table('screening_logs',
        sa.Column('screening_id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('participant_id', sa.String(length=64), nullable=False),
        sa.Column('score_english', sa.Integer(), nullable=False),
        sa.Column('score_hindi', sa.Integer(), nullable=False),
        sa.Column('passed', sa.Boolean(), nullable=False),
        sa.Column('raw_responses', sa.JSON(), nullable=False),
        sa.Column('completed_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['participant_id'], ['participants.participant_id'], ),
        sa.PrimaryKeyConstraint('screening_id'),
        sa.UniqueConstraint('participant_id')
    )

    # 4. language_background
    op.create_table('language_background',
        sa.Column('bg_id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('participant_id', sa.String(length=64), nullable=False),
        sa.Column('aoa_english', sa.Integer(), nullable=False),
        sa.Column('aoa_hindi', sa.Integer(), nullable=False),
        sa.Column('primary_home_lang', sa.String(length=64), nullable=False),
        sa.Column('medium_instruction_school', sa.String(length=64), nullable=False),
        sa.Column('medium_instruction_higher', sa.String(length=64), nullable=False),
        sa.Column('self_read_en', sa.Integer(), nullable=False),
        sa.Column('self_write_en', sa.Integer(), nullable=False),
        sa.Column('self_speak_en', sa.Integer(), nullable=False),
        sa.Column('self_read_hi', sa.Integer(), nullable=False),
        sa.Column('self_write_hi', sa.Integer(), nullable=False),
        sa.Column('self_speak_hi', sa.Integer(), nullable=False),
        sa.Column('freq_daily_en', sa.Float(), nullable=False),
        sa.Column('freq_daily_hi', sa.Float(), nullable=False),
        sa.Column('freq_daily_cs', sa.Float(), nullable=False),
        sa.Column('ai_use_en', sa.Float(), nullable=False),
        sa.Column('ai_use_hi', sa.Float(), nullable=False),
        sa.Column('ai_use_mixed', sa.Float(), nullable=False),
        sa.Column('completed_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['participant_id'], ['participants.participant_id'], ),
        sa.PrimaryKeyConstraint('bg_id'),
        sa.UniqueConstraint('participant_id')
    )

    # 5. ai_literacy
    op.create_table('ai_literacy',
        sa.Column('ails_id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('participant_id', sa.String(length=64), nullable=False),
        sa.Column('raw_responses', sa.JSON(), nullable=False),
        sa.Column('total_score', sa.Integer(), nullable=False),
        sa.Column('stratum', sa.String(length=16), nullable=False),
        sa.Column('completed_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['participant_id'], ['participants.participant_id'], ),
        sa.PrimaryKeyConstraint('ails_id'),
        sa.UniqueConstraint('participant_id')
    )

    # 6. randomization_allocations
    op.create_table('randomization_allocations',
        sa.Column('alloc_id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('participant_id', sa.String(length=64), nullable=False),
        sa.Column('stratum', sa.String(length=16), nullable=False),
        sa.Column('block_id', sa.Integer(), nullable=False),
        sa.Column('block_size', sa.Integer(), nullable=False),
        sa.Column('assigned_arm', sa.String(length=32), nullable=False),
        sa.Column('allocated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['participant_id'], ['participants.participant_id'], ),
        sa.PrimaryKeyConstraint('alloc_id'),
        sa.UniqueConstraint('participant_id')
    )

    # 7. task_sessions
    op.create_table('task_sessions',
        sa.Column('session_id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('participant_id', sa.String(length=64), nullable=False),
        sa.Column('task_id', sa.String(length=32), nullable=False),
        sa.Column('position', sa.Integer(), nullable=False),
        sa.Column('order_id', sa.Integer(), nullable=False),
        sa.Column('status', sa.String(length=32), nullable=False),
        sa.Column('started_at', sa.DateTime(), nullable=False),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['participant_id'], ['participants.participant_id'], ),
        sa.PrimaryKeyConstraint('session_id')
    )

    # 8. messages
    op.create_table('messages',
        sa.Column('message_id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('task_session_id', sa.Integer(), nullable=False),
        sa.Column('participant_id', sa.String(length=64), nullable=False),
        sa.Column('task_id', sa.String(length=32), nullable=False),
        sa.Column('sender', sa.String(length=16), nullable=False),
        sa.Column('message_text', sa.Text(), nullable=False),
        sa.Column('tokens_used', sa.Integer(), nullable=True),
        sa.Column('latency_ms', sa.Integer(), nullable=True),
        sa.Column('language_leakage_flag', sa.Boolean(), nullable=False),
        sa.Column('is_mock', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['participant_id'], ['participants.participant_id'], ),
        sa.ForeignKeyConstraint(['task_session_id'], ['task_sessions.session_id'], ),
        sa.PrimaryKeyConstraint('message_id')
    )
    op.create_index('idx_messages_session', 'messages', ['task_session_id'], unique=False)

    # 9. telemetry_events
    op.create_table('telemetry_events',
        sa.Column('event_id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('participant_id', sa.String(length=64), nullable=False),
        sa.Column('task_id', sa.String(length=32), nullable=True),
        sa.Column('timestamp', sa.DateTime(), nullable=False),
        sa.Column('event_type', sa.String(length=64), nullable=False),
        sa.Column('event_data', sa.JSON(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['participant_id'], ['participants.participant_id'], ),
        sa.PrimaryKeyConstraint('event_id')
    )
    op.create_index('idx_telemetry_participant', 'telemetry_events', ['participant_id'], unique=False)

    # 10. final_decisions
    op.create_table('final_decisions',
        sa.Column('decision_id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('task_session_id', sa.Integer(), nullable=False),
        sa.Column('participant_id', sa.String(length=64), nullable=False),
        sa.Column('task_id', sa.String(length=32), nullable=False),
        sa.Column('submitted_answers', sa.JSON(), nullable=False),
        sa.Column('confidence_score', sa.Integer(), nullable=False),
        sa.Column('calculated_score', sa.Float(), nullable=False),
        sa.Column('score_breakdown', sa.JSON(), nullable=False),
        sa.Column('submitted_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['participant_id'], ['participants.participant_id'], ),
        sa.ForeignKeyConstraint(['task_session_id'], ['task_sessions.session_id'], ),
        sa.PrimaryKeyConstraint('decision_id'),
        sa.UniqueConstraint('task_session_id')
    )

    # 11. post_task_measures
    op.create_table('post_task_measures',
        sa.Column('measure_id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('participant_id', sa.String(length=64), nullable=False),
        sa.Column('nasa_tlx_raw', sa.JSON(), nullable=False),
        sa.Column('tlx_composite_score', sa.Float(), nullable=False),
        sa.Column('feedback_comments', sa.Text(), nullable=True),
        sa.Column('submitted_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['participant_id'], ['participants.participant_id'], ),
        sa.PrimaryKeyConstraint('measure_id'),
        sa.UniqueConstraint('participant_id')
    )

    # 12. technical_errors
    op.create_table('technical_errors',
        sa.Column('error_id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('participant_id', sa.String(length=64), nullable=True),
        sa.Column('task_id', sa.String(length=32), nullable=True),
        sa.Column('error_type', sa.String(length=64), nullable=False),
        sa.Column('error_message', sa.Text(), nullable=False),
        sa.Column('context_data', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('error_id')
    )

def downgrade() -> None:
    op.drop_table('technical_errors')
    op.drop_table('post_task_measures')
    op.drop_table('final_decisions')
    op.drop_index('idx_telemetry_participant', table_name='telemetry_events')
    op.drop_table('telemetry_events')
    op.drop_index('idx_messages_session', table_name='messages')
    op.drop_table('messages')
    op.drop_table('task_sessions')
    op.drop_table('randomization_allocations')
    op.drop_table('ai_literacy')
    op.drop_table('language_background')
    op.drop_table('screening_logs')
    op.drop_table('consent_logs')
    op.drop_index(op.f('ix_participants_ip_hash'), table_name='participants')
    op.drop_table('participants')
