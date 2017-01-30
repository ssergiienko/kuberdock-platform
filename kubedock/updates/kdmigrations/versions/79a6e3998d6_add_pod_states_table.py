
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

"""Add pod states table

Revision ID: 79a6e3998d6
Revises: 3a8320be841c
Create Date: 2015-10-21 10:14:57.865340

"""

# revision identifiers, used by Alembic.
revision = '79a6e3998d6'
down_revision = '3a8320be841c'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('pod_states',
    sa.Column('pod_id', postgresql.UUID(), nullable=False),
    sa.Column('start_time', sa.DateTime(), nullable=False),
    sa.Column('end_time', sa.DateTime(), nullable=True),
    sa.Column('last_event_time', sa.DateTime(), nullable=True),
    sa.Column('last_event', sa.String(length=255), nullable=True),
    sa.Column('hostname', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['pod_id'], ['pods.id'], ),
    sa.PrimaryKeyConstraint('pod_id', 'start_time')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('pod_states')
    ### end Alembic commands ###
