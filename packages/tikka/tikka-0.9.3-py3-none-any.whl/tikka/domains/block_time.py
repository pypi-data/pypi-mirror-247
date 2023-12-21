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

from datetime import datetime, timedelta
from typing import Optional

from tikka.domains.currencies import Currencies
from tikka.domains.nodes import Nodes


class BlockTime:
    def __init__(self, currencies: Currencies, nodes: Nodes):
        """
        Initialize BlockTime domain instance

        :param currencies: Currencies domain instance
        :param nodes: Nodes domain instance
        """
        self.currencies = currencies
        self.nodes = nodes

    def get_datetime_from_block(self, block_number: int) -> Optional[datetime]:
        """
        Return a datetime object from a block number

        :param block_number: Block number
        :return:
        """
        # network access to update current block number, can be slow...
        self.nodes.network_fetch_current_node()

        current_time = datetime.now()
        node = self.nodes.get(self.nodes.get_current_url())
        if node is None:
            return None
        currency = self.currencies.get_current()
        current_block_number = node.block
        if current_block_number is None:
            return None
        block_diff = block_number - current_block_number
        if block_diff < 0:
            block_time = current_time - timedelta(
                milliseconds=abs(block_diff) * currency.block_duration
            )
        else:
            block_time = current_time + timedelta(
                milliseconds=abs(block_diff) * currency.block_duration
            )

        return block_time
