"""Create post table

Revision ID: 9ae1b3e156f6
Revises: 
Create Date: 2021-12-01 13:31:40.504517

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9ae1b3e156f6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'posts',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
    )


def downgrade():
    op.drop_table('posts')
