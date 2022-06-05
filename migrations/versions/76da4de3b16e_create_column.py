"""create column

Revision ID: 76da4de3b16e
Revises: 8f2dbda40223
Create Date: 2022-06-03 18:29:24.350862

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '76da4de3b16e'
down_revision = '8f2dbda40223'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('owner_name', sa.String(), nullable=True))
    op.add_column('posts', sa.Column('owner_email', sa.String(), nullable=True))
    op.drop_constraint('posts_owner_id_fkey', 'posts', type_='foreignkey')
    op.create_foreign_key(None, 'posts', 'users', ['owner_id'], ['id'], source_schema='core', referent_schema='core')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'posts', schema='core', type_='foreignkey')
    op.create_foreign_key('posts_owner_id_fkey', 'posts', 'users', ['owner_id'], ['id'])
    op.drop_column('posts', 'owner_email')
    op.drop_column('posts', 'owner_name')
    # ### end Alembic commands ###
