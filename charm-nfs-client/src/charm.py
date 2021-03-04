#!/usr/bin/env python3
# Copyright 2021 bdx
# See LICENSE file for licensing details.

"""Charm NFS client.

This charm provides an NFS server process, and an interface for an
NFS client to relate.
"""

import logging

from ops.charm import CharmBase
from ops.main import main

from nfs_peer import PeerRelation
from nfs_relation import NFS


logger = logging.getLogger(__name__)


class CharmNFSClient(CharmBase):
    """Charm NFS client."""

    def __init__(self, *args):
        super().__init__(*args)

        self._nfs = NFS(self, "nfs")

        self._peer = PeerRelation(self, "nfs-client-peer")

        self.framework.observe(self.on.install, self._on_install)

        self.framework.observe(self.on.start, self._on_start)

        self.framework.observe(self.on.config_changed, self._on_config_changed)

        self.framework.observe(self.on.update_status, self._on_update_status)

        self.framework.observe(self.on.upgrade_charm, self._on_upgrade_charm)

        self.framework.observe(self.on.stop, self._on_stop)

        self.framework.observe(self.on.remove, self._on_remove)

    def _on_install(self, event):
        logger.debug("####### NFS - CLIENT INSTALL EVENT")

    def _on_start(self, event):
        logger.debug("####### NFS - CLIENT START EVENT")

    def _on_config_changed(self, event):
        logger.debug("####### NFS - CLIENT CONFIG_CHANGED EVENT")

    def _on_update_status(self, event):
        logger.debug("####### NFS - CLIENT UPDATE STATUS EVENT")

    def _on_upgrade_charm(self, event):
        logger.debug("####### NFS - CLIENT UPGRADE_CHARM EVENT")

    def _on_stop(self, event):
        logger.debug("####### NFS - CLIENT STOP EVENT")

    def _on_remove(self, event):
        logger.debug("####### NFS - CLIENT REMOVE EVENT")


if __name__ == "__main__":
    main(CharmNFSClient)
