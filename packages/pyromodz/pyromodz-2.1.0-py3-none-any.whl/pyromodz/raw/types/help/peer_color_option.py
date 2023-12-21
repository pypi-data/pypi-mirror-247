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


class PeerColorOption(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~pyromodz.raw.base.help.PeerColorOption`.

    Details:
        - Layer: ``167``
        - ID: ``135BD42F``

    Parameters:
        color_id (``int`` ``32-bit``):
            N/A

        hidden (``bool``, *optional*):
            N/A

        colors (:obj:`help.PeerColorSet <pyromodz.raw.base.help.PeerColorSet>`, *optional*):
            N/A

        dark_colors (:obj:`help.PeerColorSet <pyromodz.raw.base.help.PeerColorSet>`, *optional*):
            N/A

    """

    __slots__: List[str] = ["color_id", "hidden", "colors", "dark_colors"]

    ID = 0x135bd42f
    QUALNAME = "types.help.PeerColorOption"

    def __init__(self, *, color_id: int, hidden: Optional[bool] = None, colors: "raw.base.help.PeerColorSet" = None, dark_colors: "raw.base.help.PeerColorSet" = None) -> None:
        self.color_id = color_id  # int
        self.hidden = hidden  # flags.0?true
        self.colors = colors  # flags.1?help.PeerColorSet
        self.dark_colors = dark_colors  # flags.2?help.PeerColorSet

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "PeerColorOption":
        
        flags = Int.read(b)
        
        hidden = True if flags & (1 << 0) else False
        color_id = Int.read(b)
        
        colors = TLObject.read(b) if flags & (1 << 1) else None
        
        dark_colors = TLObject.read(b) if flags & (1 << 2) else None
        
        return PeerColorOption(color_id=color_id, hidden=hidden, colors=colors, dark_colors=dark_colors)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.hidden else 0
        flags |= (1 << 1) if self.colors is not None else 0
        flags |= (1 << 2) if self.dark_colors is not None else 0
        b.write(Int(flags))
        
        b.write(Int(self.color_id))
        
        if self.colors is not None:
            b.write(self.colors.write())
        
        if self.dark_colors is not None:
            b.write(self.dark_colors.write())
        
        return b.getvalue()
