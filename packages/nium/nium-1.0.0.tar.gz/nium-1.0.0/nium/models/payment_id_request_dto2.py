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


from typing import List, Optional
from pydantic import BaseModel, Field, StrictStr, conlist, validator
from nium.models.wallet_payment_ids_tag_request_dto import WalletPaymentIdsTagRequestDTO

class PaymentIdRequestDTO2(BaseModel):
    """
    PaymentIdRequestDTO2
    """
    tags: Optional[conlist(WalletPaymentIdsTagRequestDTO)] = Field(None, description="This object contains the user defined key-value pairs provided by the client. The maximum number of tags allowed is 15.")
    account_category: Optional[StrictStr] = Field(None, alias="accountCategory", description="This field accepts the account category while assigning a virtual account")
    bank_name: StrictStr = Field(..., alias="bankName", description="This field accepts the bank name and the possible values are: BOL_LT MONOOVA_AU DBS_HK DBS_SG JPM_AU JPM_SG CB_GB CFSB_USINTL JPM_UK CITI_SG")
    currency_code: StrictStr = Field(..., alias="currencyCode", description="This field accepts the 3-letter [ISO-4217 currency code](https://www.iso.org/iso-4217-currency-codes.html).")
    __properties = ["tags", "accountCategory", "bankName", "currencyCode"]

    @validator('account_category')
    def account_category_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in ('SELF_FUNDING_ACCOUNT', 'COLLECTION_ACCOUNT', 'Null'):
            raise ValueError("must be one of enum values ('SELF_FUNDING_ACCOUNT', 'COLLECTION_ACCOUNT', 'Null')")
        return value

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
    def from_json(cls, json_str: str) -> PaymentIdRequestDTO2:
        """Create an instance of PaymentIdRequestDTO2 from a JSON string"""
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
    def from_dict(cls, obj: dict) -> PaymentIdRequestDTO2:
        """Create an instance of PaymentIdRequestDTO2 from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return PaymentIdRequestDTO2.parse_obj(obj)

        _obj = PaymentIdRequestDTO2.parse_obj({
            "tags": [WalletPaymentIdsTagRequestDTO.from_dict(_item) for _item in obj.get("tags")] if obj.get("tags") is not None else None,
            "account_category": obj.get("accountCategory"),
            "bank_name": obj.get("bankName"),
            "currency_code": obj.get("currencyCode")
        })
        return _obj


