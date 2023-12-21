#  Pyromodz - Telegram MTProto API Client Library for Python
#  Copyright (C) 2024-present Kaal-xD <https://github.com/Kaal-xD>
#
#  This file is part of Pyromodz.
#
#  Pyromodz is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyromodz is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyromodz.  If not, see <http://www.gnu.org/licenses/>.

from io import BytesIO

from pyromodz.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyromodz.raw.core import TLObject
from pyromodz import raw
from typing import List, Optional, Any

# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #


class ReadHistory(TLObject):  # type: ignore
    """Telegram API function.

    Details:
        - Layer: ``167``
        - ID: ``E306D3A``

    Parameters:
        peer (:obj:`InputPeer <pyromodz.raw.base.InputPeer>`):
            N/A

        max_id (``int`` ``32-bit``):
            N/A

    Returns:
        :obj:`messages.AffectedMessages <pyromodz.raw.base.messages.AffectedMessages>`
    """

    __slots__: List[str] = ["peer", "max_id"]

    ID = 0xe306d3a
    QUALNAME = "functions.messages.ReadHistory"

    def __init__(self, *, peer: "raw.base.InputPeer", max_id: int) -> None:
        self.peer = peer  # InputPeer
        self.max_id = max_id  # int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "ReadHistory":
        # No flags
        
        peer = TLObject.read(b)
        
        max_id = Int.read(b)
        
        return ReadHistory(peer=peer, max_id=max_id)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.peer.write())
        
        b.write(Int(self.max_id))
        
        return b.getvalue()
