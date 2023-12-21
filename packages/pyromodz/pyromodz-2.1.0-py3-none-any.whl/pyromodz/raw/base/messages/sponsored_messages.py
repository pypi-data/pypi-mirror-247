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

# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #

from typing import Union
from pyromodz import raw
from pyromodz.raw.core import TLObject

SponsoredMessages = Union[raw.types.messages.SponsoredMessages, raw.types.messages.SponsoredMessagesEmpty]


# noinspection PyRedeclaration
class SponsoredMessages:  # type: ignore
    """Telegram API base type.

    Constructors:
        This base type has 2 constructors available.

        .. currentmodule:: pyromodz.raw.types

        .. autosummary::
            :nosignatures:

            messages.SponsoredMessages
            messages.SponsoredMessagesEmpty

    Functions:
        This object can be returned by 1 function.

        .. currentmodule:: pyromodz.raw.functions

        .. autosummary::
            :nosignatures:

            channels.GetSponsoredMessages
    """

    QUALNAME = "pyromodz.raw.base.messages.SponsoredMessages"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes: "
                        "you tried to use a base type instance as argument, "
                        "but you need to instantiate one of its constructors instead. "
                        "More info: https://docs.pyromodz.org/telegram/base/sponsored-messages")
