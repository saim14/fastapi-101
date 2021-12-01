"""Add foreign key to post table

Revision ID: 624069a176b4
Revises: 2afe160856af
Create Date: 2021-12-01 14:02:32.107512

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '624069a176b4'
down_revision = '2afe160856af'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key(
        'posts_users_fk', 
        source_table='posts', 
        referent_table = 'users', 
        local_cols= ['owner_id'], 
        remote_cols = ['id'], 
        ondelete='CASCADE')


def downgrade():
    op.drop_constraint('posts_users_fk', 'posts', type_='foreignkey')
    op.drop_column('posts', 'owner_id')
