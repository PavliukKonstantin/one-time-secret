"""First

Revision ID: 9dad310fa1fd
Revises: 
Create Date: 2020-09-10 14:28:05.445280

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9dad310fa1fd'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('secret',
    sa.Column('secret_key', sa.String(length=32), nullable=False),
    sa.Column('secret_phrase', sa.Text(), nullable=False),
    sa.Column('code_phrase', sa.Text(), nullable=False),
    sa.Column('salt', sa.String(length=32), nullable=False),
    sa.Column('creation_date_time', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('secret_key')
    )
    op.create_index(op.f('ix_secret_secret_key'), 'secret', ['secret_key'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_secret_secret_key'), table_name='secret')
    op.drop_table('secret')
    # ### end Alembic commands ###