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


class NotificationSoundLocal(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~pyromodz.raw.base.NotificationSound`.

    Details:
        - Layer: ``167``
        - ID: ``830B9AE4``

    Parameters:
        title (``str``):
            N/A

        data (``str``):
            N/A

    """

    __slots__: List[str] = ["title", "data"]

    ID = 0x830b9ae4
    QUALNAME = "types.NotificationSoundLocal"

    def __init__(self, *, title: str, data: str) -> None:
        self.title = title  # string
        self.data = data  # string

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "NotificationSoundLocal":
        # No flags
        
        title = String.read(b)
        
        data = String.read(b)
        
        return NotificationSoundLocal(title=title, data=data)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.title))
        
        b.write(String(self.data))
        
        return b.getvalue()
