"""initial migration

Revision ID: 27aeaa59d8f9
Revises: 
Create Date: 2023-07-22 01:08:52.773638

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '27aeaa59d8f9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('blood_types',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=10), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('genders',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('provinces',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('regencies',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('province_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['province_id'], ['provinces.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('districts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('regency_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['regency_id'], ['regencies.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('email', sa.String(length=50), nullable=False),
    sa.Column('password', sa.String(length=100), nullable=False),
    sa.Column('role_id', sa.Integer(), nullable=False),
    sa.Column('gender_id', sa.Integer(), nullable=True),
    sa.Column('nik', sa.String(length=16), nullable=True),
    sa.Column('birthday', sa.Date(), nullable=True),
    sa.Column('blood_type_id', sa.Integer(), nullable=True),
    sa.Column('district_id', sa.Integer(), nullable=True),
    sa.Column('address', sa.String(length=100), nullable=True),
    sa.Column('latitude', sa.Float(), nullable=True),
    sa.Column('longitude', sa.Float(), nullable=True),
    sa.Column('current_latitude', sa.Float(), nullable=True),
    sa.Column('current_longitude', sa.Float(), nullable=True),
    sa.Column('phone_number', sa.String(length=20), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['blood_type_id'], ['blood_types.id'], ),
    sa.ForeignKeyConstraint(['district_id'], ['districts.id'], ),
    sa.ForeignKeyConstraint(['gender_id'], ['genders.id'], ),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('screenings',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('hb', sa.Float(precision=2), nullable=False),
    sa.Column('mch', sa.Float(precision=2), nullable=False),
    sa.Column('mcv', sa.Float(precision=2), nullable=False),
    sa.Column('probability', sa.Float(precision=2), nullable=True),
    sa.Column('dna', sa.Boolean(), nullable=True),
    sa.Column('verified', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('screenings')
    op.drop_table('users')
    op.drop_table('districts')
    op.drop_table('regencies')
    op.drop_table('roles')
    op.drop_table('provinces')
    op.drop_table('genders')
    op.drop_table('blood_types')
    # ### end Alembic commands ###
