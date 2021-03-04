#!/usr/bin/env python3
# Copyright 2021 bdx
# See LICENSE file for licensing details.

"""Relation for NFS client.

This relation provides the client side interface of the 'nfs' relation.
"""

import logging

from ops.framework import (
    EventBase, EventSource, Object, ObjectEvents, StoredState,
)

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
        logger.debug("######## NFS RELATION CREATED")

    def _on_relation_joined(self, event):
        logger.debug("######## NFS RELATION JOINED")
        server_ip = event.relation.data[event.unit]["ingress-address"]
        self._stored.server_ip = server_ip
        self.on.connect_to_server.emit()

    def _on_relation_changed(self, event):
        logger.debug("######## NFS RELATION CHANGED")

    def _on_relation_departed(self, event):
        logger.debug("######## NFS RELATION DEPARTED")

    def _on_relation_broken(self, event):
        logger.debug("######## NFS RELATION BROKEN")
        self._stored.server_ip = ""
        self.on.server_unavailable.emit()

    def get_server_ip(self):
        """Return the nfs server ip address."""
        return self._stored.server_ip
