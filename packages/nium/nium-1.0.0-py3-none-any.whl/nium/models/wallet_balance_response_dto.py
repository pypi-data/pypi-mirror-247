# coding: utf-8

"""
    NIUM Platform

    NIUM Platform

    Contact: experience@nium.com
    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json


from typing import List, Optional, Union
from pydantic import BaseModel, Field, StrictBool, StrictFloat, StrictInt, StrictStr, conlist
from nium.models.merchant_category_response_dto2 import MerchantCategoryResponseDTO2

class WalletBalanceResponseDTO(BaseModel):
    """
    WalletBalanceResponseDTO
    """
    balance: Optional[Union[StrictFloat, StrictInt]] = Field(None, description="The available amount in the pocket.")
    cur_symbol: Optional[StrictStr] = Field(None, alias="curSymbol", description="This field contains the 3-letter [ISO-4217 currency code](https://www.iso.org/iso-4217-currency-codes.html) for the pocket currency.")
    default: Optional[StrictBool] = None
    iso_code: Optional[StrictStr] = Field(None, alias="isoCode", description="The [3-digit ISO numeric code](https://www.currency-iso.org/en/home/tables/table-a1.html) for the currency.")
    mcc_data: Optional[conlist(MerchantCategoryResponseDTO2)] = Field(None, alias="mccData", description="The mccData is an array that contains multiple objects. Each object is a mccCode for which the pocket has restrictions.")
    pocket_name: Optional[StrictStr] = Field(None, alias="pocketName", description="This is the name of the pocket defined under base currency.")
    with_holding_balance: Optional[Union[StrictFloat, StrictInt]] = Field(None, alias="withHoldingBalance", description="The amount blocked by NIUM.")
    __properties = ["balance", "curSymbol", "default", "isoCode", "mccData", "pocketName", "withHoldingBalance"]

    class Config:
        """Pydantic configuration"""
        allow_population_by_field_name = True
        validate_assignment = True

    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.dict(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> WalletBalanceResponseDTO:
        """Create an instance of WalletBalanceResponseDTO from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of each item in mcc_data (list)
        _items = []
        if self.mcc_data:
            for _item in self.mcc_data:
                if _item:
                    _items.append(_item.to_dict())
            _dict['mccData'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> WalletBalanceResponseDTO:
        """Create an instance of WalletBalanceResponseDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return WalletBalanceResponseDTO.parse_obj(obj)

        _obj = WalletBalanceResponseDTO.parse_obj({
            "balance": obj.get("balance"),
            "cur_symbol": obj.get("curSymbol"),
            "default": obj.get("default"),
            "iso_code": obj.get("isoCode"),
            "mcc_data": [MerchantCategoryResponseDTO2.from_dict(_item) for _item in obj.get("mccData")] if obj.get("mccData") is not None else None,
            "pocket_name": obj.get("pocketName"),
            "with_holding_balance": obj.get("withHoldingBalance")
        })
        return _obj


