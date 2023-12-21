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


class DeleteExportedInvite(TLObject):  # type: ignore
    """Telegram API function.

    Details:
        - Layer: ``167``
        - ID: ``719C5C5E``

    Parameters:
        chatlist (:obj:`InputChatlist <pyromodz.raw.base.InputChatlist>`):
            N/A

        slug (``str``):
            N/A

    Returns:
        ``bool``
    """

    __slots__: List[str] = ["chatlist", "slug"]

    ID = 0x719c5c5e
    QUALNAME = "functions.chatlists.DeleteExportedInvite"

    def __init__(self, *, chatlist: "raw.base.InputChatlist", slug: str) -> None:
        self.chatlist = chatlist  # InputChatlist
        self.slug = slug  # string

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "DeleteExportedInvite":
        # No flags
        
        chatlist = TLObject.read(b)
        
        slug = String.read(b)
        
        return DeleteExportedInvite(chatlist=chatlist, slug=slug)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.chatlist.write())
        
        b.write(String(self.slug))
        
        return b.getvalue()
