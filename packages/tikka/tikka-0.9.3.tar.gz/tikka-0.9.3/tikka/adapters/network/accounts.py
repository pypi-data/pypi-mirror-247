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
import logging
from typing import Optional

from tikka.interfaces.adapters.network.accounts import NetworkAccountsInterface


class NetworkAccounts(NetworkAccountsInterface):
    """
    NetworkAccounts class
    """

    def get_balance(self, address: str) -> Optional[int]:
        # __doc__ = (  # pylint: disable=redefined-builtin, unused-variable
        #     NetworkAccountsInterface.get_balance.__doc__
        # )
        if not self.connections.is_connected():
            raise Exception("""Server not connected""")
        if self.connections.rpc.client is None:
            raise Exception("""Server not connected""")

        # system.account: FrameSystemAccountInfo
        # {
        #   nonce: 1
        #   consumers: 0
        #   providers: 1
        #   sufficients: 0
        #   data: {
        #     randomId: 0x18a4d...
        #     free: 9,799
        #     reserved: 0
        #     feeFrozen: 0
        #   }
        # }
        try:
            result = self.connections.rpc.client.query("System", "Account", [address])
        except Exception as exception:
            logging.exception(exception)
            raise exception

        if result.meta_info["result_found"] is False:
            return None

        return result.value["data"]["free"]

    get_balance.__doc__ = (  # pylint: disable=redefined-builtin, unused-variable
        NetworkAccountsInterface.get_balance.__doc__
    )
