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


from typing import List
from pydantic import BaseModel, Field, StrictStr, conlist
from nium.models.wallet_payment_ids_tag_request_dto2 import WalletPaymentIdsTagRequestDTO2

class PaymentIdTagRequestDTO(BaseModel):
    """
    PaymentIdTagRequestDTO
    """
    tags: conlist(WalletPaymentIdsTagRequestDTO2) = Field(..., description="This object accepts the user defined key-value pairs. The maximum number of tags allowed is 15.")
    currency_code: StrictStr = Field(..., alias="currencyCode", description="This field accepts the 3-letter [ISO-4217 currency code](https://www.iso.org/iso-4217-currency-codes.html).")
    unique_payment_id: StrictStr = Field(..., alias="uniquePaymentId", description="This field contains the unique virtual account assigned to customer.")
    __properties = ["tags", "currencyCode", "uniquePaymentId"]

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
    def from_json(cls, json_str: str) -> PaymentIdTagRequestDTO:
        """Create an instance of PaymentIdTagRequestDTO from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of each item in tags (list)
        _items = []
        if self.tags:
            for _item in self.tags:
                if _item:
                    _items.append(_item.to_dict())
            _dict['tags'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> PaymentIdTagRequestDTO:
        """Create an instance of PaymentIdTagRequestDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return PaymentIdTagRequestDTO.parse_obj(obj)

        _obj = PaymentIdTagRequestDTO.parse_obj({
            "tags": [WalletPaymentIdsTagRequestDTO2.from_dict(_item) for _item in obj.get("tags")] if obj.get("tags") is not None else None,
            "currency_code": obj.get("currencyCode"),
            "unique_payment_id": obj.get("uniquePaymentId")
        })
        return _obj


