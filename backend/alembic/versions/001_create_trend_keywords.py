"""create trend_keywords table

Revision ID: 001_create_trend_keywords
Revises: 
Create Date: 2026-10-24 12:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

revision = '001_create_trend_keywords'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        'trend_keywords',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('keyword', sa.String(length=255), nullable=False),
        sa.Column('normalized_tokens', sa.String(length=255), nullable=False),
        sa.Column('category_name', sa.String(length=100), nullable=False),
        sa.Column('monthly_searches', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('growth_pct', sa.Float(), nullable=True, server_default='0.0'),
        sa.Column('source', sa.String(length=50), nullable=True, server_default='Google PK'),
        sa.Column('exists_in_store', sa.Boolean(), nullable=True, server_default=sa.text('false')),
        sa.Column('matched_wc_product_id', sa.Integer(), nullable=True),
        sa.Column('last_scanned_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_trend_keywords_id'), 'trend_keywords', ['id'], unique=False)
    op.create_index(op.f('ix_trend_keywords_keyword'), 'trend_keywords', ['keyword'], unique=True)
    op.create_index(op.f('ix_trend_keywords_category_name'), 'trend_keywords', ['category_name'], unique=False)
    op.create_index(op.f('ix_trend_keywords_exists_in_store'), 'trend_keywords', ['exists_in_store'], unique=False)

def downgrade() -> None:
    op.drop_index(op.f('ix_trend_keywords_exists_in_store'), table_name='trend_keywords')
    op.drop_index(op.f('ix_trend_keywords_category_name'), table_name='trend_keywords')
    op.drop_index(op.f('ix_trend_keywords_keyword'), table_name='trend_keywords')
    op.drop_index(op.f('ix_trend_keywords_id'), table_name='trend_keywords')
    op.drop_table('trend_keywords')

