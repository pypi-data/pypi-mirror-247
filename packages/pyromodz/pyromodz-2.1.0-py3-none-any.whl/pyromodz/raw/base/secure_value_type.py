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

SecureValueType = Union[raw.types.SecureValueTypeAddress, raw.types.SecureValueTypeBankStatement, raw.types.SecureValueTypeDriverLicense, raw.types.SecureValueTypeEmail, raw.types.SecureValueTypeIdentityCard, raw.types.SecureValueTypeInternalPassport, raw.types.SecureValueTypePassport, raw.types.SecureValueTypePassportRegistration, raw.types.SecureValueTypePersonalDetails, raw.types.SecureValueTypePhone, raw.types.SecureValueTypeRentalAgreement, raw.types.SecureValueTypeTemporaryRegistration, raw.types.SecureValueTypeUtilityBill]


# noinspection PyRedeclaration
class SecureValueType:  # type: ignore
    """Telegram API base type.

    Constructors:
        This base type has 13 constructors available.

        .. currentmodule:: pyromodz.raw.types

        .. autosummary::
            :nosignatures:

            SecureValueTypeAddress
            SecureValueTypeBankStatement
            SecureValueTypeDriverLicense
            SecureValueTypeEmail
            SecureValueTypeIdentityCard
            SecureValueTypeInternalPassport
            SecureValueTypePassport
            SecureValueTypePassportRegistration
            SecureValueTypePersonalDetails
            SecureValueTypePhone
            SecureValueTypeRentalAgreement
            SecureValueTypeTemporaryRegistration
            SecureValueTypeUtilityBill
    """

    QUALNAME = "pyromodz.raw.base.SecureValueType"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes: "
                        "you tried to use a base type instance as argument, "
                        "but you need to instantiate one of its constructors instead. "
                        "More info: https://docs.pyromodz.org/telegram/base/secure-value-type")
