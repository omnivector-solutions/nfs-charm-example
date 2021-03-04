#!/usr/bin/env python3
# Copyright 2021 bdx
# See LICENSE file for licensing details.

"""Charm NFS server.

This charm provides an NFS server process, and an interface for an
NFS client to relate.
"""

import logging

from ops.charm import CharmBase
from ops.main import main

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
        logger.debug("####### NFS SERVER INSTALL EVENT")

    def _on_start(self, event):
        logger.debug("####### NFS SERVER START EVENT")

    def _on_config_changed(self, event):
        logger.debug("####### NFS SERVER CONFIG_CHANGED EVENT")

    def _on_update_status(self, event):
        logger.debug("####### NFS SERVER UPDATE_STATUS EVENT")

    def _on_upgrade_charm(self, event):
        logger.debug("####### NFS SERVER UPGRADE_CHARM EVENT")

    def _on_stop(self, event):
        logger.debug("####### NFS SERVER STOP EVENT")

    def _on_remove(self, event):
        logger.debug("####### NFS SERVER REMOVE EVENT")

if __name__ == "__main__":
    main(CharmNFSServer)
