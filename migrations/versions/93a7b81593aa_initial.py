"""initial

Revision ID: 93a7b81593aa
Revises: 
Create Date: 2022-05-30 11:48:14.657841

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '93a7b81593aa'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    schema='core'
    )
    op.create_table('posts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('owner_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['core.users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='core'
    )
    op.create_index(op.f('ix_core_posts_title'), 'posts', ['title'], unique=False, schema='core')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_core_posts_title'), table_name='posts', schema='core')
    op.drop_table('posts', schema='core')
    op.drop_table('users', schema='core')
    # ### end Alembic commands ###
