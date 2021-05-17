"""delete alphabet quiz table

Revision ID: b54580a8fc88
Revises: 6a5687644997
Create Date: 2021-05-16 12:31:52.873156

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b54580a8fc88'
down_revision = '6a5687644997'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('alphabet_quiz')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('alphabet_quiz',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('testee_id', sa.INTEGER(), nullable=True),
    sa.Column('q1', sa.INTEGER(), nullable=True),
    sa.Column('q2', sa.INTEGER(), nullable=True),
    sa.Column('q3', sa.VARCHAR(length=4), nullable=True),
    sa.Column('q4', sa.VARCHAR(length=4), nullable=True),
    sa.Column('score', sa.FLOAT(), nullable=True),
    sa.ForeignKeyConstraint(['testee_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###