"""create pricing_audits table

Revision ID: 003_create_pricing_audits
Revises: 002_create_supplier_offers
Create Date: 2026-10-24 12:10:00.000000
"""
from alembic import op
import sqlalchemy as sa

revision = '003_create_pricing_audits'
down_revision = '002_create_supplier_offers'
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        'pricing_audits',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('supplier_offer_id', sa.Integer(), nullable=False),
        sa.Column('wholesale_cost_pkr', sa.Float(), nullable=False),
        sa.Column('min_40_pkr', sa.Float(), nullable=False),
        sa.Column('max_50_pkr', sa.Float(), nullable=False),
        sa.Column('competitor_prices_json', sa.Text(), nullable=True),
        sa.Column('market_avg_pkr', sa.Float(), nullable=False),
        sa.Column('recommended_sale_pkr', sa.Float(), nullable=False),
        sa.Column('recommended_regular_pkr', sa.Float(), nullable=False),
        sa.Column('net_profit_pkr', sa.Float(), nullable=False),
        sa.Column('profit_margin_pct', sa.Float(), nullable=False),
        sa.Column('strategy_note', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['supplier_offer_id'], ['supplier_offers.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_pricing_audits_id'), 'pricing_audits', ['id'], unique=False)

def downgrade() -> None:
    op.drop_index(op.f('ix_pricing_audits_id'), table_name='pricing_audits')
    op.drop_table('pricing_audits')

