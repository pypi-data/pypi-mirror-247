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


class InputKeyboardButtonUserProfile(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~pyromodz.raw.base.KeyboardButton`.

    Details:
        - Layer: ``167``
        - ID: ``E988037B``

    Parameters:
        text (``str``):
            N/A

        user_id (:obj:`InputUser <pyromodz.raw.base.InputUser>`):
            N/A

    """

    __slots__: List[str] = ["text", "user_id"]

    ID = 0xe988037b
    QUALNAME = "types.InputKeyboardButtonUserProfile"

    def __init__(self, *, text: str, user_id: "raw.base.InputUser") -> None:
        self.text = text  # string
        self.user_id = user_id  # InputUser

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "InputKeyboardButtonUserProfile":
        # No flags
        
        text = String.read(b)
        
        user_id = TLObject.read(b)
        
        return InputKeyboardButtonUserProfile(text=text, user_id=user_id)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.text))
        
        b.write(self.user_id.write())
        
        return b.getvalue()
