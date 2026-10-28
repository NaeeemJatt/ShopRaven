"""create restock_waitlists table

Revision ID: 005_create_restock_waitlists
Revises: 004_create_wc_products_sync
Create Date: 2026-10-24 12:20:00.000000
"""
from alembic import op
import sqlalchemy as sa

revision = '005_create_restock_waitlists'
down_revision = '004_create_wc_products_sync'
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        'restock_waitlists',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('wc_product_id', sa.Integer(), nullable=False),
        sa.Column('product_title', sa.String(length=300), nullable=False),
        sa.Column('customer_whatsapp', sa.String(length=50), nullable=False),
        sa.Column('notified', sa.Boolean(), nullable=True, server_default=sa.text('false')),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('checkout_link_sent_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_restock_waitlists_id'), 'restock_waitlists', ['id'], unique=False)
    op.create_index(op.f('ix_restock_waitlists_wc_product_id'), 'restock_waitlists', ['wc_product_id'], unique=False)
    op.create_index(op.f('ix_restock_waitlists_customer_whatsapp'), 'restock_waitlists', ['customer_whatsapp'], unique=False)
    op.create_index(op.f('ix_restock_waitlists_notified'), 'restock_waitlists', ['notified'], unique=False)

def downgrade() -> None:
    op.drop_index(op.f('ix_restock_waitlists_notified'), table_name='restock_waitlists')
    op.drop_index(op.f('ix_restock_waitlists_customer_whatsapp'), table_name='restock_waitlists')
    op.drop_index(op.f('ix_restock_waitlists_wc_product_id'), table_name='restock_waitlists')
    op.drop_index(op.f('ix_restock_waitlists_id'), table_name='restock_waitlists')
    op.drop_table('restock_waitlists')

