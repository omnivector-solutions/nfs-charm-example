#!/usr/bin/env python3
# Copyright 2021 bdx
# See LICENSE file for licensing details.

"""Charm NFS client.

This charm provides an NFS server process, and an interface for an
NFS client to relate.
"""

import logging
import subprocess

from ops.charm import CharmBase
from ops.main import main
from ops.model import ActiveStatus, BlockedStatus

from ops.framework import (
    EventBase, EventSource, Object, ObjectEvents, StoredState,
)

from fstab import Fstab


logger = logging.getLogger(__name__)


class NFSServerAvailableEvent(EventBase):
    """Emit this when an NFS server joins the relation."""


class NFSServerUnavailableEvent(EventBase):
    """Emit this when an NFS server is no longer available."""


class NFSClientEvents(ObjectEvents):
    """Emit when an nfs server joins the relation."""
    connect_to_server = EventSource(NFSServerAvailableEvent)
    server_unavailable = EventSource(NFSServerUnavailableEvent)


class NFS(Object):
    """NFS client relation interface."""

    _stored = StoredState()
    on = NFSClientEvents()

    def __init__(self, charm, relation_name):
        super().__init__(charm, relation_name)

        self._charm = charm
        self._relation_name = relation_name

        self._stored.set_default(
            server_ip=str(),
        )

        self.framework.observe(
            self._charm.on[self._relation_name].relation_joined,
            self._on_relation_joined,
        )

        self.framework.observe(
            self._charm.on[self._relation_name].relation_broken,
            self._on_relation_broken,
        )

    def _on_relation_joined(self, event):
        server_ip = event.relation.data[event.unit]["ingress-address"]
        self._stored.server_ip = server_ip
        self.on.connect_to_server.emit()

    def _on_relation_broken(self, event):
        self._stored.server_ip = ""
        self.on.server_unavailable.emit()

    def get_server_ip(self):
        """Return the nfs server ip address."""
        return self._stored.server_ip


class CharmNfsClient(CharmBase):
    """Charm NFS client."""

    _stored = StoredState()

    def __init__(self, *args):
        super().__init__(*args)

        self._stored.set_default(mount_point=str())

        self._nfs = NFS(self, "nfs")

        self.framework.observe(self.on.install, self._on_install)
        self.framework.observe(self.on.update_status, self._on_update_status)
        self.framework.observe(
            self._nfs.on.connect_to_server,
            self._on_connect_to_server
        )
        self.framework.observe(
            self._nfs.on.server_unavailable,
            self._on_nfs_unavailable
        )

    def _on_install(self, event):
        """Install the NFS client and create the dir to be mouted."""
        subprocess.call(["apt", "update"])
        subprocess.call(["apt", "install", "nfs-common", "-y"])
        subprocess.call(["mkdir", "/srv/slurm", "-p"])
        self._on_update_status(event)

    def _on_connect_to_server(self, event):
        """Connect to an NFS server.

        Obtain the server ip address and create fstab entry.
        """
        # Obtain the server ip address from the stored object in the interface
        server_ip = self._nfs.get_server_ip()
        mount_src = f"{server_ip}:/srv/slurm"
        mount_dest = "/srv/slurm"

        nfs_mount_point = _mount_nfs(mount_src, mount_dest)

        if not nfs_mount_point["mounted"]:
            self.unit.status = BlockedStatus("NFS mount unsuccessful")
            logger.debug(f"cannot mount nfs, {nfs_mount_point['reason']}")
            return

        # Add the mount entry to /etc/fstab
        Fstab.add(mount_src, mount_dest, filesystem="nfs")

        # Store the server_ip and update status
        self._set_mount_point(mount_src)
        self._on_update_status(event)

    def _on_nfs_unavailable(self, event):
        """Communicate the NFS server no longer exists to the user."""
        Fstab.remove_by_mountpoint(self._get_mount_point())
        self._set_mount_point("")
        self._on_update_status(event)

    def _on_update_status(self, event):
        server_ip = self._nfs.get_server_ip()
        if server_ip:
            self.unit.status = ActiveStatus("nfs share available")
        else:
            self.unit.status = BlockedStatus("Need relation to NFS server.")

    def _get_mount_point(self):
        return self._stored.mount_point

    def _set_mount_point(self, mount_point):
        self._stored.mount_point = mount_point


def _mount_nfs(src, dest) -> dict:
    # Run the command to mount the nfs share
    mount_out = subprocess.check_output([
        "mount",
        src,
        dest,
    ]).decode().strip()

    ret = dict()

    if mount_out != "":
        ret["mounted"] = False
        ret["reason"] = mount_out
    else:
        ret["mounted"] = True
        ret["reason"] = mount_out

    return ret


if __name__ == "__main__":
    main(CharmNfsClient)
