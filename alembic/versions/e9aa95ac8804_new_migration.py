"""New Migration

Revision ID: e9aa95ac8804
Revises: baa9097006be
Create Date: 2025-03-21 10:19:52.849249

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e9aa95ac8804'
down_revision = 'baa9097006be'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create Users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('username', sa.String, unique=True, nullable=False),
        sa.Column('email', sa.String, unique=True, nullable=False),
        sa.Column('birthdate', sa.Date, nullable=False),
        sa.Column('password', sa.String, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=sa.func.now())
    )

    # Create Author table
    op.create_table(
        'author',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String),
        sa.Column('age', sa.Integer),
        sa.Column('time_created', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('time_updated', sa.DateTime(timezone=True), onupdate=sa.func.now())
    )

    # Create Book table with Foreign Key
    op.create_table(
        'book',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('title', sa.String),
        sa.Column('rating', sa.Float),
        sa.Column('time_created', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('time_updated', sa.DateTime(timezone=True), onupdate=sa.func.now()),
        sa.Column('author_id', sa.Integer, sa.ForeignKey('author.id', ondelete='CASCADE'))
    )


def downgrade() -> None:
    # Drop tables in reverse order to prevent foreign key constraint issues
    op.drop_table('book')
    op.drop_table('author')
    op.drop_table('users')
