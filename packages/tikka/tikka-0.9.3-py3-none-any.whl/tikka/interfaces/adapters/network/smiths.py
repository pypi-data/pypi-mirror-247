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
from typing import List, Optional

from substrateinterface import Keypair

from tikka.domains.entities.smith import SmithCertification, SmithMembership
from tikka.interfaces.domains.connections import ConnectionsInterface


class NetworkSmithsInterface(abc.ABC):
    """
    NetworkSmithsInterface class
    """

    def __init__(self, connections: ConnectionsInterface) -> None:
        """
        Use connections to request/send smiths information

        :param connections: ConnectionsInterface instance
        :return:
        """
        self.connections = connections

    @abc.abstractmethod
    def request_membership(self, keypair: Keypair, session_keys: str) -> bool:
        """
        Request a smith membership for the Keypair account with node session_keys

        :param keypair: Owner Keypair
        :param session_keys: Session public keys (hex string "0x123XYZ")
        :return:
        """
        raise NotImplementedError

    @abc.abstractmethod
    def claim_membership(self, keypair: Keypair) -> bool:
        """
        Claim that last smith membership request for the Keypair account fulfill all requirements

        :param keypair: Owner Keypair
        :return:
        """
        raise NotImplementedError

    @abc.abstractmethod
    def revoke_membership(self, keypair: Keypair) -> bool:
        """
        Revoke smith membership for the Keypair account

        :param keypair: Owner Keypair
        :return:
        """
        raise NotImplementedError

    @abc.abstractmethod
    def membership(self, identity_index: int) -> Optional[SmithMembership]:
        """
        Return SmithMembership instance

        :return:
        """
        raise NotImplementedError

    @abc.abstractmethod
    def pending_membership(self, identity_index: int) -> bool:
        """
        Return True if identity status is pending_membership

        :return:
        """
        raise NotImplementedError

    @abc.abstractmethod
    def certs_by_receiver(
        self, receiver_address: str, receiver_identity_index: int
    ) -> Optional[List[SmithCertification]]:
        """
        Return a list of certification received by identity_index

         [
         [identity index, expire on block number],
         [identity index, expire on block number]
         ]

        :param receiver_address: Address of account receiving certs
        :param receiver_identity_index: Index of identity receiving certs
        :return:
        """
        raise NotImplementedError
