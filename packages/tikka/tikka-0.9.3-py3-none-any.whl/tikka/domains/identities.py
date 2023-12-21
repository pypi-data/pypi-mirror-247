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
from typing import Optional

from substrateinterface import Keypair

from tikka.domains.entities.identity import STATUS_CREATED, STATUS_VALIDATED, Identity
from tikka.interfaces.adapters.network.identities import NetworkIdentitiesInterface
from tikka.interfaces.adapters.repository.identities import (
    IdentitiesRepositoryInterface,
)


class Identities:

    """
    Identities domain class
    """

    def __init__(
        self,
        repository: IdentitiesRepositoryInterface,
        network: NetworkIdentitiesInterface,
    ):
        """
        Init Accounts domain

        :param repository: AccountsRepositoryInterface instance
        :param network: NetworkAccountsInterface instance
        """
        self.repository = repository
        self.network = network

    @staticmethod
    def create(
        index: int,
        removable_on: int,
        next_creatable_on: int,
        status: str = STATUS_CREATED,
    ):
        """
        Return an identity instance from params

        :param index: Index number in blockchain
        :param removable_on: Identity expiration timestamp
        :param next_creatable_on: Date after which a new identity can be created
        :param status: Identity status
        :return:
        """
        return Identity(
            index=index,
            removable_on=removable_on,
            next_creatable_on=next_creatable_on,
            status=status,
        )

    def add(self, identity: Identity):
        """
        Add identity in repository

        :param identity: Identity instance
        :return:
        """
        self.repository.add(identity)

    def update(self, identity: Identity):
        """
        Update identity in repository

        :param identity: Identity instance
        :return:
        """
        self.repository.update(identity)

    def get(self, index: int) -> Optional[Identity]:
        """
        Get identity instance

        :param index: Identity index
        :return:
        """
        return self.repository.get(index)

    def delete(self, index: int) -> None:
        """
        Delete identity in repository

        :param index: Identity index to delete
        :return:
        """
        self.repository.delete(index)

    def exists(self, index: int) -> bool:
        """
        Return True if identity exists in repository

        :param index: Identity index to check
        :return:
        """
        return self.repository.exists(index)

    def is_validated(self, index: int) -> bool:
        """
        Return True if identity status is validated

        :param index: Identity index to check
        :return:
        """
        identity = self.get(index)
        if identity is None:
            return False
        return identity.status == STATUS_VALIDATED

    def fetch_index_from_network(self, address: str) -> Optional[int]:
        """
        Fetch account identity index from network if any

        :param address: Account address
        :return:
        """
        return self.network.get_identity_index(address)

    def fetch_from_network(self, index: int) -> Optional[Identity]:
        """
        Fetch Identity instance by index from network if any

        :param index: Identity index
        :return:
        """
        identity = self.network.get_identity(index)
        if identity is not None:
            if self.exists(index) is True:
                self.update(identity)
            else:
                self.add(identity)

        return identity

    def change_owner_key(self, old_keypair: Keypair, new_keypair: Keypair) -> bool:
        """
        Change identity owner from old_keypair to new_keypair

        :param old_keypair: Keypair of current identity account
        :param new_keypair: Keypair of new identity account
        :return:
        """
        return self.network.change_owner_key(old_keypair, new_keypair)
