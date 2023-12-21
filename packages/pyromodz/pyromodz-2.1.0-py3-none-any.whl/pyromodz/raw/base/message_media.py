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

MessageMedia = Union[raw.types.MessageMediaContact, raw.types.MessageMediaDice, raw.types.MessageMediaDocument, raw.types.MessageMediaEmpty, raw.types.MessageMediaGame, raw.types.MessageMediaGeo, raw.types.MessageMediaGeoLive, raw.types.MessageMediaGiveaway, raw.types.MessageMediaInvoice, raw.types.MessageMediaPhoto, raw.types.MessageMediaPoll, raw.types.MessageMediaStory, raw.types.MessageMediaUnsupported, raw.types.MessageMediaVenue, raw.types.MessageMediaWebPage]


# noinspection PyRedeclaration
class MessageMedia:  # type: ignore
    """Telegram API base type.

    Constructors:
        This base type has 15 constructors available.

        .. currentmodule:: pyromodz.raw.types

        .. autosummary::
            :nosignatures:

            MessageMediaContact
            MessageMediaDice
            MessageMediaDocument
            MessageMediaEmpty
            MessageMediaGame
            MessageMediaGeo
            MessageMediaGeoLive
            MessageMediaGiveaway
            MessageMediaInvoice
            MessageMediaPhoto
            MessageMediaPoll
            MessageMediaStory
            MessageMediaUnsupported
            MessageMediaVenue
            MessageMediaWebPage

    Functions:
        This object can be returned by 3 functions.

        .. currentmodule:: pyromodz.raw.functions

        .. autosummary::
            :nosignatures:

            messages.GetWebPagePreview
            messages.UploadMedia
            messages.UploadImportedMedia
    """

    QUALNAME = "pyromodz.raw.base.MessageMedia"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes: "
                        "you tried to use a base type instance as argument, "
                        "but you need to instantiate one of its constructors instead. "
                        "More info: https://docs.pyromodz.org/telegram/base/message-media")
