#!/usr/bin/env python3
# Copyright 2021 bdx
# See LICENSE file for licensing details.

"""Charm NFS server.

This charm provides an NFS server process, and an interface for an
NFS client to relate.
"""

import logging
import subprocess

from pathlib import Path

from ops.charm import CharmBase
from ops.main import main
from ops.model import ActiveStatus, BlockedStatus
from ops.framework import Object

logger = logging.getLogger(__name__)


class NFS(Object):
    """NFS client relation interface."""

    def __init__(self, charm, relation_name):
        super().__init__(charm, relation_name)
        self._charm = charm
        self._relation_name = relation_name
        self.framework.observe(
            self._charm.on[self._relation_name].relation_created,
            self._on_relation_created
        )
        self.framework.observe(
            self._charm.on[self._relation_name].relation_joined,
            self._on_relation_joined
        )
        self.framework.observe(
            self._charm.on[self._relation_name].relation_changed,
            self._on_relation_changed
        )
        self.framework.observe(
            self._charm.on[self._relation_name].relation_departed,
            self._on_relation_departed
        )
        self.framework.observe(
            self._charm.on[self._relation_name].relation_broken,
            self._on_relation_broken
        )

    def _on_relation_created(self, event):
        pass

    def _on_relation_joined(self, event):
        pass

    def _on_relation_changed(self, event):
        pass

    def _on_relation_departed(self, event):
        pass

    def _on_relation_broken(self, event):
        pass


class CharmNfsServerCharm(CharmBase):
    """Charm NFS server."""

    def __init__(self, *args):
        """Observe charm events."""
        super().__init__(*args)

        self._nfs = NFS(self, "nfs")

        self.framework.observe(self.on.install, self._on_install)
        self.framework.observe(self.on.update_status, self._on_update_status)

    def _on_install(self, event):
        """Install the NFS server."""
        shared_mount_point = "/srv/slurm"
        subprocess.call(["apt", "install", "nfs-kernel-server", "-y"])
        subprocess.call(["mkdir", shared_mount_point, "-p"])
        subprocess.call(["chown", "nobody:nogroup", shared_mount_point])
        subprocess.call(["chmod", "777", shared_mount_point])

        nfs_exports_path = Path("/etc/exports")
        if nfs_exports_path.exists():
            nfs_exports_path.unlink()

        nfs_exports_path.write_text(
            f"{shared_mount_point}  *(rw,sync,no_subtree_check)"
        )

        subprocess.call(["exportfs", "-a"])
        subprocess.call(["systemctl", "restart", "nfs-kernel-server"])

        self._on_update_status(event)

    def _on_update_status(self, event):
        """"Update the unit status."""
        if not _is_nfs_available():
            self.unit.status = BlockedStatus(
                "nfs server cannot start, please debug"
            )
            return

        self.unit.status = ActiveStatus("nfs server available")


def _is_nfs_available() -> bool:
    is_nfs_available = subprocess.check_output([
        "systemctl", "is-active", "nfs-kernel-server"
    ]).decode().strip()

    if "inactive" in is_nfs_available:
        return False

    return True


if __name__ == "__main__":
    main(CharmNfsServerCharm)
