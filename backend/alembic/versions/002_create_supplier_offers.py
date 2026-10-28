"""create supplier_offers table

Revision ID: 002_create_supplier_offers
Revises: 001_create_trend_keywords
Create Date: 2026-10-24 12:05:00.000000
"""
from alembic import op
import sqlalchemy as sa

revision = '002_create_supplier_offers'
down_revision = '001_create_trend_keywords'
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        'supplier_offers',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('trend_keyword_id', sa.Integer(), nullable=True),
        sa.Column('supplier_name', sa.String(length=50), nullable=False),
        sa.Column('supplier_url', sa.String(length=500), nullable=False),
        sa.Column('supplier_sku', sa.String(length=100), nullable=False),
        sa.Column('product_title', sa.String(length=300), nullable=False),
        sa.Column('wholesale_cost_pkr', sa.Float(), nullable=False),
        sa.Column('in_stock', sa.Boolean(), nullable=True, server_default=sa.text('true')),
        sa.Column('raw_description', sa.Text(), nullable=True),
        sa.Column('specs_json', sa.Text(), nullable=True),
        sa.Column('image_urls_json', sa.Text(), nullable=True),
        sa.Column('scraped_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['trend_keyword_id'], ['trend_keywords.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_supplier_offers_id'), 'supplier_offers', ['id'], unique=False)
    op.create_index(op.f('ix_supplier_offers_supplier_sku'), 'supplier_offers', ['supplier_sku'], unique=False)
    op.create_index(op.f('ix_supplier_offers_in_stock'), 'supplier_offers', ['in_stock'], unique=False)

def downgrade() -> None:
    op.drop_index(op.f('ix_supplier_offers_in_stock'), table_name='supplier_offers')
    op.drop_index(op.f('ix_supplier_offers_supplier_sku'), table_name='supplier_offers')
    op.drop_index(op.f('ix_supplier_offers_id'), table_name='supplier_offers')
    op.drop_table('supplier_offers')

