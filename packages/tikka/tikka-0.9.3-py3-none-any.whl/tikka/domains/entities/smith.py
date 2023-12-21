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

from dataclasses import dataclass
from typing import Optional, TypeVar

SmithType = TypeVar("SmithType", bound="Smith")


@dataclass
class SmithMembership:
    expire_on: int


@dataclass
class Smith:
    identity_index: int
    membership: Optional[SmithMembership]
    pending_membership: bool


@dataclass
class SmithCertification:
    issuer_identity_index: int
    issuer_address: str
    receiver_identity_index: int
    receiver_address: str
    expire_on_block: int
