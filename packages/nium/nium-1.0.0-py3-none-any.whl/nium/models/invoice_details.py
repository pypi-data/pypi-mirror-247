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
from nium.models.item_details import ItemDetails

class InvoiceDetails(BaseModel):
    """
    InvoiceDetails
    """
    var_date: Optional[StrictStr] = Field(None, alias="date", description="date of the trade")
    description: Optional[StrictStr] = Field(None, description="string without special characters")
    items: Optional[conlist(ItemDetails)] = Field(None, description="contains quantity and price information")
    name: Optional[StrictStr] = Field(None, description="string without special characters")
    number: Optional[StrictStr] = Field(None, description="alphanumeric value containing invoice number")
    __properties = ["date", "description", "items", "name", "number"]

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
    def from_json(cls, json_str: str) -> InvoiceDetails:
        """Create an instance of InvoiceDetails from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of each item in items (list)
        _items = []
        if self.items:
            for _item in self.items:
                if _item:
                    _items.append(_item.to_dict())
            _dict['items'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> InvoiceDetails:
        """Create an instance of InvoiceDetails from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return InvoiceDetails.parse_obj(obj)

        _obj = InvoiceDetails.parse_obj({
            "var_date": obj.get("date"),
            "description": obj.get("description"),
            "items": [ItemDetails.from_dict(_item) for _item in obj.get("items")] if obj.get("items") is not None else None,
            "name": obj.get("name"),
            "number": obj.get("number")
        })
        return _obj


