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
from pydantic import BaseModel, Field, StrictStr, conlist
from nium.models.transaction_limit_dto import TransactionLimitDTO

class TransactionLimitsDTO(BaseModel):
    """
    TransactionLimitsDTO
    """
    card_hash_id: Optional[StrictStr] = Field(None, alias="cardHashId", description="Unique card identifier generated while new/add-on card issuance.")
    transaction_limits: conlist(TransactionLimitDTO) = Field(..., alias="transactionLimits", description="This array contains an object for each card limit parameter. This object contains the below data elements. Please refer the example for exact structure.")
    __properties = ["cardHashId", "transactionLimits"]

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
    def from_json(cls, json_str: str) -> TransactionLimitsDTO:
        """Create an instance of TransactionLimitsDTO from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of each item in transaction_limits (list)
        _items = []
        if self.transaction_limits:
            for _item in self.transaction_limits:
                if _item:
                    _items.append(_item.to_dict())
            _dict['transactionLimits'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> TransactionLimitsDTO:
        """Create an instance of TransactionLimitsDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return TransactionLimitsDTO.parse_obj(obj)

        _obj = TransactionLimitsDTO.parse_obj({
            "card_hash_id": obj.get("cardHashId"),
            "transaction_limits": [TransactionLimitDTO.from_dict(_item) for _item in obj.get("transactionLimits")] if obj.get("transactionLimits") is not None else None
        })
        return _obj


