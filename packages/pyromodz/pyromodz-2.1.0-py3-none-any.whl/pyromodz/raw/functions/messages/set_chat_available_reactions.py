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


class SetChatAvailableReactions(TLObject):  # type: ignore
    """Telegram API function.

    Details:
        - Layer: ``167``
        - ID: ``FEB16771``

    Parameters:
        peer (:obj:`InputPeer <pyromodz.raw.base.InputPeer>`):
            N/A

        available_reactions (:obj:`ChatReactions <pyromodz.raw.base.ChatReactions>`):
            N/A

    Returns:
        :obj:`Updates <pyromodz.raw.base.Updates>`
    """

    __slots__: List[str] = ["peer", "available_reactions"]

    ID = 0xfeb16771
    QUALNAME = "functions.messages.SetChatAvailableReactions"

    def __init__(self, *, peer: "raw.base.InputPeer", available_reactions: "raw.base.ChatReactions") -> None:
        self.peer = peer  # InputPeer
        self.available_reactions = available_reactions  # ChatReactions

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "SetChatAvailableReactions":
        # No flags
        
        peer = TLObject.read(b)
        
        available_reactions = TLObject.read(b)
        
        return SetChatAvailableReactions(peer=peer, available_reactions=available_reactions)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.peer.write())
        
        b.write(self.available_reactions.write())
        
        return b.getvalue()
