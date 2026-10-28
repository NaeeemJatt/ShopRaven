"""create analytics_snapshots table

Revision ID: 007_create_analytics_snapshots
Revises: 006_create_customer_segments
Create Date: 2026-10-24 12:30:00.000000
"""
from alembic import op
import sqlalchemy as sa

revision = '007_create_analytics_snapshots'
down_revision = '006_create_customer_segments'
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        'analytics_snapshots',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('snapshot_date', sa.Date(), nullable=False),
        sa.Column('total_visitors', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('new_visitors', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('returning_visitors', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('gross_sales_pkr', sa.Float(), nullable=True, server_default='0.0'),
        sa.Column('shipping_collected_pkr', sa.Float(), nullable=True, server_default='0.0'),
        sa.Column('supplier_cost_pkr', sa.Float(), nullable=True, server_default='0.0'),
        sa.Column('net_profit_pkr', sa.Float(), nullable=True, server_default='0.0'),
        sa.Column('total_orders', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('delivered_orders', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('in_transit_orders', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('rto_orders', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('aeo_referrals', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('city_breakdown_json', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_analytics_snapshots_id'), 'analytics_snapshots', ['id'], unique=False)
    op.create_index(op.f('ix_analytics_snapshots_snapshot_date'), 'analytics_snapshots', ['snapshot_date'], unique=True)

def downgrade() -> None:
    op.drop_index(op.f('ix_analytics_snapshots_snapshot_date'), table_name='analytics_snapshots')
    op.drop_index(op.f('ix_analytics_snapshots_id'), table_name='analytics_snapshots')
    op.drop_table('analytics_snapshots')

