"""create wc_products_sync table

Revision ID: 004_create_wc_products_sync
Revises: 003_create_pricing_audits
Create Date: 2026-10-24 12:15:00.000000
"""
from alembic import op
import sqlalchemy as sa

revision = '004_create_wc_products_sync'
down_revision = '003_create_pricing_audits'
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        'wc_products_sync',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('wc_product_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=300), nullable=False),
        sa.Column('slug', sa.String(length=300), nullable=False),
        sa.Column('category_name', sa.String(length=100), nullable=False),
        sa.Column('supplier_name', sa.String(length=50), nullable=True),
        sa.Column('supplier_sku', sa.String(length=100), nullable=True),
        sa.Column('wholesale_cost_pkr', sa.Float(), nullable=True),
        sa.Column('sale_price_pkr', sa.Float(), nullable=False),
        sa.Column('regular_price_pkr', sa.Float(), nullable=False),
        sa.Column('net_profit_pkr', sa.Float(), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=True, server_default='draft'),
        sa.Column('menu_order', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('total_views', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('total_orders', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('conversion_rate', sa.Float(), nullable=True, server_default='0.0'),
        sa.Column('redirect_target_url', sa.String(length=500), nullable=True),
        sa.Column('json_ld_schema', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_wc_products_sync_id'), 'wc_products_sync', ['id'], unique=False)
    op.create_index(op.f('ix_wc_products_sync_wc_product_id'), 'wc_products_sync', ['wc_product_id'], unique=True)
    op.create_index(op.f('ix_wc_products_sync_slug'), 'wc_products_sync', ['slug'], unique=False)
    op.create_index(op.f('ix_wc_products_sync_category_name'), 'wc_products_sync', ['category_name'], unique=False)
    op.create_index(op.f('ix_wc_products_sync_status'), 'wc_products_sync', ['status'], unique=False)
    op.create_index(op.f('ix_wc_products_sync_menu_order'), 'wc_products_sync', ['menu_order'], unique=False)

def downgrade() -> None:
    op.drop_index(op.f('ix_wc_products_sync_menu_order'), table_name='wc_products_sync')
    op.drop_index(op.f('ix_wc_products_sync_status'), table_name='wc_products_sync')
    op.drop_index(op.f('ix_wc_products_sync_category_name'), table_name='wc_products_sync')
    op.drop_index(op.f('ix_wc_products_sync_slug'), table_name='wc_products_sync')
    op.drop_index(op.f('ix_wc_products_sync_wc_product_id'), table_name='wc_products_sync')
    op.drop_index(op.f('ix_wc_products_sync_id'), table_name='wc_products_sync')
    op.drop_table('wc_products_sync')

