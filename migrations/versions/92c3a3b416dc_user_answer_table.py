"""user answer table

Revision ID: 92c3a3b416dc
Revises: 15b60c634b96
Create Date: 2021-05-15 12:51:52.640685

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '92c3a3b416dc'
down_revision = '15b60c634b96'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_answer',
    sa.Column('quiz_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('ans1', sa.String(length=20), nullable=True),
    sa.Column('ans2', sa.String(length=20), nullable=True),
    sa.Column('ans3', sa.String(length=20), nullable=True),
    sa.Column('ans4', sa.String(length=20), nullable=True),
    sa.Column('ans5', sa.String(length=20), nullable=True),
    sa.Column('ans6', sa.String(length=20), nullable=True),
    sa.Column('ans7', sa.String(length=20), nullable=True),
    sa.Column('ans8', sa.String(length=20), nullable=True),
    sa.Column('score', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['quiz_id'], ['quiz.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('quiz_id', 'user_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_answer')
    # ### end Alembic commands ###
