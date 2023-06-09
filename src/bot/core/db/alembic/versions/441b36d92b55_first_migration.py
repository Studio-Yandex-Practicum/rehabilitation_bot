"""First migration

Revision ID: 441b36d92b55
Revises:
Create Date: 2023-06-30 13:10:04.605357

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '441b36d92b55'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('message_data',
    sa.Column('text', sa.String(), nullable=True),
    sa.Column('sticker', sa.String(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('obscene_words',
    sa.Column('word', sa.String(length=25), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('word')
    )
    op.create_table('message_filter_data',
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('sticker_count', sa.Integer(), nullable=False),
    sa.Column('last_message_id', sa.Integer(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['last_message_id'], ['message_data.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('message_filter_data')
    op.drop_table('obscene_words')
    op.drop_table('message_data')
    # ### end Alembic commands ###
