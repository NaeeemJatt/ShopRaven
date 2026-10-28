"""create customer_segments table

Revision ID: 006_create_customer_segments
Revises: 005_create_restock_waitlists
Create Date: 2026-10-24 12:25:00.000000
"""
from alembic import op
import sqlalchemy as sa

revision = '006_create_customer_segments'
down_revision = '005_create_restock_waitlists'
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        'customer_segments',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('phone_or_email', sa.String(length=100), nullable=False),
        sa.Column('city', sa.String(length=100), nullable=True),
        sa.Column('total_orders', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('delivered_orders', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('rto_orders', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('total_spent_pkr', sa.Float(), nullable=True, server_default='0.0'),
        sa.Column('segment_tag', sa.String(length=50), nullable=True, server_default='NEW_VISITOR'),
        sa.Column('last_coupon_code', sa.String(length=50), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_customer_segments_id'), 'customer_segments', ['id'], unique=False)
    op.create_index(op.f('ix_customer_segments_phone_or_email'), 'customer_segments', ['phone_or_email'], unique=True)
    op.create_index(op.f('ix_customer_segments_segment_tag'), 'customer_segments', ['segment_tag'], unique=False)

def downgrade() -> None:
    op.drop_index(op.f('ix_customer_segments_segment_tag'), table_name='customer_segments')
    op.drop_index(op.f('ix_customer_segments_phone_or_email'), table_name='customer_segments')
    op.drop_index(op.f('ix_customer_segments_id'), table_name='customer_segments')
    op.drop_table('customer_segments')

