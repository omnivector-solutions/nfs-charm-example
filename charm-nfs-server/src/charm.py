#!/usr/bin/env python3
# Copyright 2021 bdx
# See LICENSE file for licensing details.

"""Charm NFS server.

This charm provides an NFS server process, and an interface for an
NFS client to relate.
"""

import logging
import subprocess

# from pathlib import Path

from ops.charm import CharmBase
from ops.main import main
# from ops.model import ActiveStatus, BlockedStatus

from nfs_relation import NFS
from nfs_peer import PeerRelation


logger = logging.getLogger(__name__)


class CharmNFSServer(CharmBase):
    """Charm NFS server."""

    def __init__(self, *args):
        """Observe charm events."""
        super().__init__(*args)

        self._nfs = NFS(self, "nfs")
        self._peer = PeerRelation(self, "nfs-peer")

        self.framework.observe(self.on.install, self._on_install)

        self.framework.observe(self.on.start, self._on_start)

        self.framework.observe(self.on.config_changed, self._on_config_changed)

        self.framework.observe(self.on.update_status, self._on_update_status)

        self.framework.observe(self.on.upgrade_charm, self._on_upgrade_charm)

        self.framework.observe(self.on.stop, self._on_stop)

        self.framework.observe(self.on.remove, self._on_remove)

    def _on_install(self, event):
        """Install the NFS server."""
#        shared_mount_point = "/srv/slurm"
#        subprocess.call(["apt", "install", "nfs-kernel-server", "-y"])
#        subprocess.call(["mkdir", shared_mount_point, "-p"])
#        subprocess.call(["chown", "nobody:nogroup", shared_mount_point])
#        subprocess.call(["chmod", "777", shared_mount_point])
#
#        nfs_exports_path = Path("/etc/exports")
#        if nfs_exports_path.exists():
#            nfs_exports_path.unlink()
#
#        nfs_exports_path.write_text(
#            f"{shared_mount_point}  *(rw,sync,no_subtree_check)"
#        )
#
#        subprocess.call(["exportfs", "-a"])
#        subprocess.call(["systemctl", "restart", "nfs-kernel-server"])
#
#        self._on_update_status(event)
        logger.debug("####### NFS SERVER INSTALL EVENT")

    def _on_start(self, event):
        logger.debug("####### NFS SERVER START EVENT")

    def _on_config_changed(self, event):
        logger.debug("####### NFS SERVER CONFIG_CHANGED EVENT")

    def _on_upgrade_charm(self, event):
        logger.debug("####### NFS SERVER UPGRADE_CHARM EVENT")

    def _on_stop(self, event):
        logger.debug("####### NFS SERVER STOP EVENT")

    def _on_remove(self, event):
        logger.debug("####### NFS SERVER REMOVE EVENT")

    def _on_update_status(self, event):
        """"Update the unit status."""
#        if not _is_nfs_available():
#            self.unit.status = BlockedStatus(
#                "nfs server cannot start, please debug"
#            )
#            return
#
#        self.unit.status = ActiveStatus("nfs server available")
        logger.debug("####### NFS SERVER UPDATE_STATUS EVENT")


def _is_nfs_available() -> bool:
    is_nfs_available = subprocess.check_output([
        "systemctl", "is-active", "nfs-kernel-server"
    ]).decode().strip()

    if "inactive" in is_nfs_available:
        return False

    return True


if __name__ == "__main__":
    main(CharmNFSServer)
