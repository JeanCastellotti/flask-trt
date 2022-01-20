"""empty message

Revision ID: d46c1515f821
Revises: 95c6cfb63b2d
Create Date: 2022-01-19 22:23:29.522089

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd46c1515f821'
down_revision = '95c6cfb63b2d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('candidates', 'resume_file',
               existing_type=sa.VARCHAR(length=50),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('candidates', 'resume_file',
               existing_type=sa.VARCHAR(length=50),
               nullable=False)
    # ### end Alembic commands ###