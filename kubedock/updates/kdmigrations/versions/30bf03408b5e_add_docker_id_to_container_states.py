
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

"""Add docker_id to container_states

Revision ID: 30bf03408b5e
Revises: 382d3b1e63aa
Create Date: 2015-09-10 08:54:37.590889

"""

# revision identifiers, used by Alembic.
revision = '30bf03408b5e'
down_revision = '382d3b1e63aa'

import logging
from alembic import op
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session as BaseSession
from sqlalchemy.dialects import postgresql
import requests

logger = logging.getLogger(__name__)

Session = sessionmaker()
Base = declarative_base()

class ContainerState(Base):
    __tablename__ = 'container_states'
    pod_id = sa.Column(postgresql.UUID, primary_key=True)
    container_name = sa.Column(sa.String(length=255), primary_key=True)
    docker_id = sa.Column(sa.String(length=80), primary_key=True)
    end_time = sa.Column(sa.DateTime, nullable=True)


def upgrade():
    bind = op.get_bind()
    session = Session(bind=bind)
    
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        'container_states',
        sa.Column('docker_id', sa.String(length=80), server_default='unknown',
                  nullable=False)
    )
    op.execute("ALTER TABLE container_states DROP CONSTRAINT container_states_pkey, "\
               "ADD CONSTRAINT container_states_pkey PRIMARY KEY "\
                    "(pod_id, container_name, docker_id, kubes, start_time);")
    # op.execute()
    try:
        # Try to get docker_id for current container states.
        # 1. Extract all DB states without end time
        # 2. Get pods information for those containers from kubes-api
        # 3. Set docker_id for selected DB-states
        states = session.query(ContainerState).filter(
            ContainerState.end_time == None)
        containers = {
            (item.pod_id, item.container_name): item for item in states
        }
        container_ids = _get_container_ids()
        for key, state in containers:
            if key not in container_ids:
                continue
            state.docker_id = container_ids[key]
        session.commit()
    except Exception as err:
        # We will not break the migration in case of failed update of
        # some docker_id fields. Just warn about it.
        logger.warning(
            u'Failed to set actual docker_id for currently running containers: %s',
            err)
        
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.execute("ALTER TABLE container_states DROP CONSTRAINT container_states_pkey, "\
               "ADD CONSTRAINT container_states_pkey PRIMARY KEY "\
                    "(pod_id, container_name, kubes, start_time);")
    op.drop_column('container_states', 'docker_id')
    ### end Alembic commands ###


def _get_container_ids():
    """Requests all pods from kubes-API."""

    from kubedock.utils import get_api_url

    url = get_api_url('pods', namespace=False, watch=False)
    req = requests.get(url)
    data = req.json()
    pods = data.get('items', [])
    res = {}
    for item in pods:
        uid = item.get('metadata', {}).get('uid')
        if not uid:
            continue
        status = item.get('status', {})
        if status.get('phase') != 'Running':
            # skip pods&containers wich are not running, because we need
            # will fill docker_id only for running containers
            continue
        cont_statuses = status.get('containerStatuses', [])
        res.update({
            (uid, cs.get('name')): cs.get('containerID')
            for cs in cont_statuses
        })
    return res
