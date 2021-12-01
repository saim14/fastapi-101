"""Add others column of posts table

Revision ID: 21aca019c49b
Revises: 624069a176b4
Create Date: 2021-12-01 14:08:24.828775

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '21aca019c49b'
down_revision = '624069a176b4'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')))


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
