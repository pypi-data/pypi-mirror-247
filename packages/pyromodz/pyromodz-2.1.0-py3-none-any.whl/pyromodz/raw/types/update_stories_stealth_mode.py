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


class UpdateStoriesStealthMode(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~pyromodz.raw.base.Update`.

    Details:
        - Layer: ``167``
        - ID: ``2C084DC1``

    Parameters:
        stealth_mode (:obj:`StoriesStealthMode <pyromodz.raw.base.StoriesStealthMode>`):
            N/A

    """

    __slots__: List[str] = ["stealth_mode"]

    ID = 0x2c084dc1
    QUALNAME = "types.UpdateStoriesStealthMode"

    def __init__(self, *, stealth_mode: "raw.base.StoriesStealthMode") -> None:
        self.stealth_mode = stealth_mode  # StoriesStealthMode

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "UpdateStoriesStealthMode":
        # No flags
        
        stealth_mode = TLObject.read(b)
        
        return UpdateStoriesStealthMode(stealth_mode=stealth_mode)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.stealth_mode.write())
        
        return b.getvalue()
