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


class SetCallRating(TLObject):  # type: ignore
    """Telegram API function.

    Details:
        - Layer: ``167``
        - ID: ``59EAD627``

    Parameters:
        peer (:obj:`InputPhoneCall <pyromodz.raw.base.InputPhoneCall>`):
            N/A

        rating (``int`` ``32-bit``):
            N/A

        comment (``str``):
            N/A

        user_initiative (``bool``, *optional*):
            N/A

    Returns:
        :obj:`Updates <pyromodz.raw.base.Updates>`
    """

    __slots__: List[str] = ["peer", "rating", "comment", "user_initiative"]

    ID = 0x59ead627
    QUALNAME = "functions.phone.SetCallRating"

    def __init__(self, *, peer: "raw.base.InputPhoneCall", rating: int, comment: str, user_initiative: Optional[bool] = None) -> None:
        self.peer = peer  # InputPhoneCall
        self.rating = rating  # int
        self.comment = comment  # string
        self.user_initiative = user_initiative  # flags.0?true

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "SetCallRating":
        
        flags = Int.read(b)
        
        user_initiative = True if flags & (1 << 0) else False
        peer = TLObject.read(b)
        
        rating = Int.read(b)
        
        comment = String.read(b)
        
        return SetCallRating(peer=peer, rating=rating, comment=comment, user_initiative=user_initiative)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.user_initiative else 0
        b.write(Int(flags))
        
        b.write(self.peer.write())
        
        b.write(Int(self.rating))
        
        b.write(String(self.comment))
        
        return b.getvalue()
