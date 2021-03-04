#!/usr/bin/env python3
# Copyright 2021 bdx
# See LICENSE file for licensing details.

"""Relation for NFS client peer.

This relation provides the peer relation.
"""

import logging

from ops.framework import Object


logger = logging.getLogger(__name__)


class PeerRelation(Object):
    """NFS client peers relation interface."""

    def __init__(self, charm, relation_name):
        super().__init__(charm, relation_name)

        self._charm = charm
        self._relation_name = relation_name

        self.framework.observe(
            self._charm.on[self._relation_name].relation_created,
            self._on_relation_created,
        )

        self.framework.observe(
            self._charm.on[self._relation_name].relation_joined,
            self._on_relation_joined,
        )

        self.framework.observe(
            self._charm.on[self._relation_name].relation_changed,
            self._on_relation_changed,
        )

        self.framework.observe(
            self._charm.on[self._relation_name].relation_departed,
            self._on_relation_departed,
        )

        self.framework.observe(
            self._charm.on[self._relation_name].relation_broken,
            self._on_relation_broken,
        )

    def _on_relation_created(self, event):
        logger.debug("##### NFS_SERVER_PEER RELATION CREATED EVENT")

    def _on_relation_joined(self, event):
        logger.debug("##### NFS_SERVER_PEER RELATION JOINED EVENT")

    def _on_relation_changed(self, event):
        logger.debug("##### NFS_SERVER_PEER RELATION CHANGED EVENT")

    def _on_relation_departed(self, event):
        logger.debug("##### NFS_SERVER_PEER RELATION DEPARTED EVENT")

    def _on_relation_broken(self, event):
        logger.debug("##### NFS_SERVER_PEER RELATION BROKEN EVENT")
