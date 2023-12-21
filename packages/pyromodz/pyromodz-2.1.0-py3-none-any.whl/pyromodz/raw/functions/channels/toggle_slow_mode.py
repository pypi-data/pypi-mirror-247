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


class ToggleSlowMode(TLObject):  # type: ignore
    """Telegram API function.

    Details:
        - Layer: ``167``
        - ID: ``EDD49EF0``

    Parameters:
        channel (:obj:`InputChannel <pyromodz.raw.base.InputChannel>`):
            N/A

        seconds (``int`` ``32-bit``):
            N/A

    Returns:
        :obj:`Updates <pyromodz.raw.base.Updates>`
    """

    __slots__: List[str] = ["channel", "seconds"]

    ID = 0xedd49ef0
    QUALNAME = "functions.channels.ToggleSlowMode"

    def __init__(self, *, channel: "raw.base.InputChannel", seconds: int) -> None:
        self.channel = channel  # InputChannel
        self.seconds = seconds  # int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "ToggleSlowMode":
        # No flags
        
        channel = TLObject.read(b)
        
        seconds = Int.read(b)
        
        return ToggleSlowMode(channel=channel, seconds=seconds)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.channel.write())
        
        b.write(Int(self.seconds))
        
        return b.getvalue()
