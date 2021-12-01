"""Add user table

Revision ID: 2afe160856af
Revises: 9dae55f25734
Create Date: 2021-12-01 13:53:14.817691

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.schema import UniqueConstraint


# revision identifiers, used by Alembic.
revision = '2afe160856af'
down_revision = '9dae55f25734'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users', 
        sa.Column('id', sa.Integer, nullable=False),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('password', sa.String(255), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )


def downgrade():
    op.drop_table('users')
