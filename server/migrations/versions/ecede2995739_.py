"""empty message

Revision ID: ecede2995739
Revises: 
Create Date: 2024-02-01 18:43:09.352388

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ecede2995739'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('messages',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('messages')
    # ### end Alembic commands ###