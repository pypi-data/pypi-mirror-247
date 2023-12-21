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

from substrateinterface import Keypair
from substrateinterface.exceptions import SubstrateRequestException

from tikka.interfaces.adapters.network.authorities import NetworkAuthoritiesInterface


class NetworkAuthorities(NetworkAuthoritiesInterface):
    """
    NetworkAuthorities class
    """

    def rotate_keys(self) -> Optional[str]:
        __doc__ = (  # pylint: disable=redefined-builtin, unused-variable
            NetworkAuthoritiesInterface.rotate_keys.__doc__
        )
        if not self.connections.is_connected():
            return None
        if self.connections.rpc.client is None:
            return None

        try:
            result = self.connections.rpc.client.rpc_request(
                "author_rotateKeys", []
            ).get("result")
        except Exception as exception:
            logging.exception(exception)
            return None

        return result

    def has_session_keys(self, session_keys: str) -> Optional[bool]:
        __doc__ = (  # pylint: disable=redefined-builtin, unused-variable
            NetworkAuthoritiesInterface.has_session_keys.__doc__
        )
        if not self.connections.is_connected():
            return None
        if self.connections.rpc.client is None:
            return None

        try:
            result = self.connections.rpc.client.rpc_request(
                "author_hasSessionKeys", [session_keys]
            ).get("result")
        except Exception as exception:
            logging.exception(exception)
            return None

        return result

    def publish_session_keys(self, keypair: Keypair, session_keys: str) -> bool:
        __doc__ = (  # pylint: disable=redefined-builtin, unused-variable
            NetworkAuthoritiesInterface.publish_session_keys.__doc__
        )
        if not self.connections.is_connected() or self.connections.rpc.client is None:
            return False

        session_keys_bytearray = bytearray.fromhex(session_keys[2:])
        params = {
            "keys": {
                "grandpa": f"0x{session_keys_bytearray[0:32].hex()}",
                "babe": f"0x{session_keys_bytearray[32:64].hex()}",
                "im_online": f"0x{session_keys_bytearray[64:96].hex()}",
                "authority_discovery": f"0x{session_keys_bytearray[96:128].hex()}",
            }
        }

        try:
            call = self.connections.rpc.client.compose_call(
                call_module="AuthorityMembers",
                call_function="set_session_keys",
                call_params=params,
            )
        except Exception as exception:
            logging.exception(exception)
            return False

        try:
            extrinsic = self.connections.rpc.client.create_signed_extrinsic(
                call=call, keypair=keypair
            )
        except Exception as exception:
            logging.exception(exception)
            return False

        try:
            # fixme: code stuck infinitely if no blocks are created on blockchain
            #       should have a timeout option
            result = self.connections.rpc.client.submit_extrinsic(
                extrinsic, wait_for_inclusion=True
            )
            logging.debug(
                "Extrinsic '%s' sent and included in block '%s'",
                result.extrinsic_hash,
                result.block_hash,
            )
        except SubstrateRequestException as exception:
            logging.exception(exception)
            return False

        if result.is_success is False:
            logging.error(result.error_message)

        return result.is_success

    def go_online(self, keypair: Keypair) -> bool:
        __doc__ = (  # pylint: disable=redefined-builtin, unused-variable
            NetworkAuthoritiesInterface.go_online.__doc__
        )
        if not self.connections.is_connected() or self.connections.rpc.client is None:
            return False

        try:
            call = self.connections.rpc.client.compose_call(
                call_module="AuthorityMembers",
                call_function="go_online",
                call_params=None,
            )
        except Exception as exception:
            logging.exception(exception)
            return False

        try:
            extrinsic = self.connections.rpc.client.create_signed_extrinsic(
                call=call, keypair=keypair
            )
        except Exception as exception:
            logging.exception(exception)
            return False

        try:
            # fixme: code stuck infinitely if no blocks are created on blockchain
            #       should have a timeout option
            result = self.connections.rpc.client.submit_extrinsic(
                extrinsic, wait_for_inclusion=True
            )
            logging.debug(
                "Extrinsic '%s' sent and included in block '%s'",
                result.extrinsic_hash,
                result.block_hash,
            )
        except SubstrateRequestException as exception:
            logging.exception(exception)
            return False

        if result.is_success is False:
            logging.error(result.error_message)

        return result.is_success

    def go_offline(self, keypair: Keypair) -> bool:
        __doc__ = (  # pylint: disable=redefined-builtin, unused-variable
            NetworkAuthoritiesInterface.go_offline.__doc__
        )
        if not self.connections.is_connected() or self.connections.rpc.client is None:
            return False

        try:
            call = self.connections.rpc.client.compose_call(
                call_module="AuthorityMembers",
                call_function="go_offline",
                call_params=None,
            )
        except Exception as exception:
            logging.exception(exception)
            return False

        try:
            extrinsic = self.connections.rpc.client.create_signed_extrinsic(
                call=call, keypair=keypair
            )
        except Exception as exception:
            logging.exception(exception)
            return False

        try:
            # fixme: code stuck infinitely if no blocks are created on blockchain
            #       should have a timeout option
            result = self.connections.rpc.client.submit_extrinsic(
                extrinsic, wait_for_inclusion=True
            )
            logging.debug(
                "Extrinsic '%s' sent and included in block '%s'",
                result.extrinsic_hash,
                result.block_hash,
            )
        except SubstrateRequestException as exception:
            logging.exception(exception)
            return False

        if result.is_success is False:
            logging.error(result.error_message)

        return result.is_success

    def is_online(self, identity_index: int) -> Optional[bool]:
        __doc__ = (  # pylint: disable=redefined-builtin, unused-variable
            NetworkAuthoritiesInterface.is_online.__doc__
        )
        if not self.connections.is_connected():
            return None
        if self.connections.rpc.client is None:
            return None

        try:
            result = self.connections.rpc.client.query(
                "AuthorityMembers", "OnlineAuthorities"
            )
        except Exception as exception:
            logging.exception(exception)
            return None

        return identity_index in result.value

    def is_incoming(self, identity_index: int) -> Optional[bool]:
        __doc__ = (  # pylint: disable=redefined-builtin, unused-variable
            NetworkAuthoritiesInterface.is_incoming.__doc__
        )
        if not self.connections.is_connected():
            return None
        if self.connections.rpc.client is None:
            return None

        try:
            result = self.connections.rpc.client.query(
                "AuthorityMembers", "IncomingAuthorities"
            )
        except Exception as exception:
            logging.exception(exception)
            return None

        return identity_index in result.value

    def is_outgoing(self, identity_index: int) -> Optional[bool]:
        __doc__ = (  # pylint: disable=redefined-builtin, unused-variable
            NetworkAuthoritiesInterface.is_outgoing.__doc__
        )
        if not self.connections.is_connected():
            return None
        if self.connections.rpc.client is None:
            return None

        try:
            result = self.connections.rpc.client.query(
                "AuthorityMembers", "OutgoingAuthorities"
            )
        except Exception as exception:
            logging.exception(exception)
            return None

        return identity_index in result.value
