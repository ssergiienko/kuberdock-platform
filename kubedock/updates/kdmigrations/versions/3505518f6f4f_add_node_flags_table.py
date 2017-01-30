
# KuberDock - is a platform that allows users to run applications using Docker
# container images and create SaaS / PaaS based on these applications.
# Copyright (C) 2017 Cloud Linux INC
#
# This file is part of KuberDock.
#
# KuberDock is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# KuberDock is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with KuberDock; if not, see <http://www.gnu.org/licenses/>.

"""Add node flags table

Revision ID: 3505518f6f4f
Revises: 79a6e3998d6
Create Date: 2015-10-29 18:03:45.928635

"""

# revision identifiers, used by Alembic.
revision = '3505518f6f4f'
down_revision = '79a6e3998d6'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('node_flags',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('deleted', sa.DateTime(), nullable=True),
    sa.Column('node_id', sa.Integer(), nullable=True),
    sa.Column('flag_name', sa.String(length=63), nullable=False),
    sa.Column('flag_value', sa.String(length=127), nullable=True),
    sa.ForeignKeyConstraint(['node_id'], [u'nodes.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_deleted_node_id_flag_name', 'node_flags', ['deleted', 'node_id', 'flag_name'], unique=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_deleted_node_id_flag_name', table_name='node_flags')
    op.drop_table('node_flags')
    ### end Alembic commands ###
