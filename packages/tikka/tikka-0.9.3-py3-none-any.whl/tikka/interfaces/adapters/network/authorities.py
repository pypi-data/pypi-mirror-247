# Copyright 2021 Vincent Texier <vit@free.fr>
#
# This software is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import abc
from typing import Optional

from substrateinterface import Keypair

from tikka.interfaces.domains.connections import ConnectionsInterface


class NetworkAuthoritiesInterface(abc.ABC):
    """
    NetworkAuthoritiesInterface class
    """

    def __init__(self, connections: ConnectionsInterface) -> None:
        """
        Use connections to request/send online authorities information

        :param connections: ConnectionsInterface instance
        :return:
        """
        self.connections = connections

    @abc.abstractmethod
    def rotate_keys(self) -> Optional[str]:
        """
        Rotate Session keys

        :return:
        """
        raise NotImplementedError

    @abc.abstractmethod
    def has_session_keys(self, session_keys: str) -> Optional[bool]:
        """
        Return True if the current node keystore store private session keys corresponding to public session_keys

        :param session_keys: Session public keys (hex string "0x123XYZ")
        :return:
        """
        raise NotImplementedError

    @abc.abstractmethod
    def publish_session_keys(self, keypair: Keypair, session_keys: str) -> bool:
        """
        Set/Change in blockchain the session public keys for the Keypair account

        :param keypair: Owner Keypair
        :param session_keys: Session public keys (hex string "0x123XYZ")
        :return:
        """
        raise NotImplementedError

    @abc.abstractmethod
    def go_online(self, keypair: Keypair) -> bool:
        """
        Start writing blocks with smith account from keypair

        :param keypair: Smith account Keypair
        :return:
        """
        raise NotImplementedError

    @abc.abstractmethod
    def go_offline(self, keypair: Keypair) -> bool:
        """
        Stop writing blocks with smith account from keypair

        :param keypair: Smith account Keypair
        :return:
        """
        raise NotImplementedError

    @abc.abstractmethod
    def is_online(self, identity_index: int) -> Optional[bool]:
        """
        Return True if identity_index is in online authorities

        :param identity_index: Identity index
        :return:
        """
        raise NotImplementedError

    @abc.abstractmethod
    def is_incoming(self, identity_index: int) -> Optional[bool]:
        """
        Return True if identity_index is in incoming authorities

        :param identity_index: Identity index
        :return:
        """
        raise NotImplementedError

    @abc.abstractmethod
    def is_outgoing(self, identity_index: int) -> Optional[bool]:
        """
        Return True if identity_index is in outgoing authorities

        :param identity_index: Identity index
        :return:
        """
        raise NotImplementedError
