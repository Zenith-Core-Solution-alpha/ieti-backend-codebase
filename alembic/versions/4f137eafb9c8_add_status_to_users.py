"""Add status to users

Revision ID: 4f137eafb9c8
Revises: e9aa95ac8804
Create Date: 2025-03-24 10:22:21.956955

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '4f137eafb9c8'
down_revision = 'e9aa95ac8804'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ✅ Add the Enum type first
    user_status = sa.Enum('pending', 'approved', name='user_status')
    user_status.create(op.get_bind(), checkfirst=True)

    # ✅ Add the `status` column to the `users` table
    op.add_column(
        'users',
        sa.Column('status', user_status, nullable=False, server_default='pending')
    )


def downgrade() -> None:
    # ✅ Remove the `status` column during downgrade
    op.drop_column('users', 'status')

    # ✅ Drop the Enum type
    sa.Enum(name='user_status').drop(op.get_bind(), checkfirst=True)
