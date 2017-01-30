
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

from .. import kdclick
from ..kdclick.access import USER, ADMIN
from ..utils import SimpleCommand


@kdclick.group('stats', available_for=(ADMIN, USER))
@kdclick.pass_obj
def stat(obj):
    """Commands for statistic management"""
    obj.executor = obj.kdctl.stats


@stat.command(available_for=USER)
@kdclick.argument('pod_id', type=str)
@kdclick.pass_obj
class Pod(SimpleCommand):
    """Get statistics of the pod"""
    pass


@stat.command(available_for=(ADMIN, USER))
@kdclick.argument('node_id', type=str)
@kdclick.pass_obj
class Node(SimpleCommand):
    """Get statistics of the container"""
    pass


@stat.command(available_for=USER)
@kdclick.argument('pod_id', type=str)
@kdclick.argument('container_id', type=str)
@kdclick.pass_obj
class Container(SimpleCommand):
    """Get statistics of the node"""
    pass
