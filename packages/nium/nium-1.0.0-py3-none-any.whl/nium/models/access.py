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
from nium.models.account import Account
from nium.models.balance import Balance
from nium.models.transaction import Transaction

class Access(BaseModel):
    """
    Access
    """
    accounts: Optional[conlist(Account)] = Field(None, description="This is an array which holds account detail fields.")
    all_psd2: Optional[StrictStr] = Field(None, alias="allPsd2", description="Only \"allAccounts\" value is admitted.")
    available_accounts: Optional[StrictStr] = Field(None, alias="availableAccounts", description="Only \"allAccounts\" or \"allAccountsWithBalances\" values are admitted")
    balances: Optional[conlist(Balance)] = Field(None, description="This is an array which holds balance detail fields.")
    transactions: Optional[conlist(Transaction)] = Field(None, description="This is an array which holds transaction detail fields.")
    __properties = ["accounts", "allPsd2", "availableAccounts", "balances", "transactions"]

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
    def from_json(cls, json_str: str) -> Access:
        """Create an instance of Access from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of each item in accounts (list)
        _items = []
        if self.accounts:
            for _item in self.accounts:
                if _item:
                    _items.append(_item.to_dict())
            _dict['accounts'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in balances (list)
        _items = []
        if self.balances:
            for _item in self.balances:
                if _item:
                    _items.append(_item.to_dict())
            _dict['balances'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in transactions (list)
        _items = []
        if self.transactions:
            for _item in self.transactions:
                if _item:
                    _items.append(_item.to_dict())
            _dict['transactions'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> Access:
        """Create an instance of Access from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return Access.parse_obj(obj)

        _obj = Access.parse_obj({
            "accounts": [Account.from_dict(_item) for _item in obj.get("accounts")] if obj.get("accounts") is not None else None,
            "all_psd2": obj.get("allPsd2"),
            "available_accounts": obj.get("availableAccounts"),
            "balances": [Balance.from_dict(_item) for _item in obj.get("balances")] if obj.get("balances") is not None else None,
            "transactions": [Transaction.from_dict(_item) for _item in obj.get("transactions")] if obj.get("transactions") is not None else None
        })
        return _obj


