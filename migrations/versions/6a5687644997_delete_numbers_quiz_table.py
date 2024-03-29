"""delete numbers quiz table

Revision ID: 6a5687644997
Revises: 92c3a3b416dc
Create Date: 2021-05-16 12:30:12.197430

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6a5687644997'
down_revision = '92c3a3b416dc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('numbers_quiz')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('numbers_quiz',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('testee_id', sa.INTEGER(), nullable=True),
    sa.Column('q1', sa.INTEGER(), nullable=True),
    sa.Column('q2', sa.VARCHAR(length=10), nullable=True),
    sa.Column('q3', sa.INTEGER(), nullable=True),
    sa.Column('q4', sa.VARCHAR(length=10), nullable=True),
    sa.Column('score', sa.FLOAT(), nullable=True),
    sa.ForeignKeyConstraint(['testee_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
