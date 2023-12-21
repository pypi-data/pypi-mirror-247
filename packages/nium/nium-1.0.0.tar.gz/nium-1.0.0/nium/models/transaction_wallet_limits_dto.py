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
from pydantic import BaseModel, Field, conlist
from nium.models.transaction_limits_dto import TransactionLimitsDTO

class TransactionWalletLimitsDTO(BaseModel):
    """
    TransactionWalletLimitsDTO
    """
    transaction_wallet_limits: Optional[conlist(TransactionLimitsDTO)] = Field(None, alias="transactionWalletLimits", description="This array contains all the limits applicable for each card.")
    __properties = ["transactionWalletLimits"]

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
    def from_json(cls, json_str: str) -> TransactionWalletLimitsDTO:
        """Create an instance of TransactionWalletLimitsDTO from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of each item in transaction_wallet_limits (list)
        _items = []
        if self.transaction_wallet_limits:
            for _item in self.transaction_wallet_limits:
                if _item:
                    _items.append(_item.to_dict())
            _dict['transactionWalletLimits'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> TransactionWalletLimitsDTO:
        """Create an instance of TransactionWalletLimitsDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return TransactionWalletLimitsDTO.parse_obj(obj)

        _obj = TransactionWalletLimitsDTO.parse_obj({
            "transaction_wallet_limits": [TransactionLimitsDTO.from_dict(_item) for _item in obj.get("transactionWalletLimits")] if obj.get("transactionWalletLimits") is not None else None
        })
        return _obj


