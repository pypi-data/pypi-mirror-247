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


from typing import Optional
from pydantic import BaseModel, Field, StrictStr

class ItemDetails(BaseModel):
    """
    ItemDetails
    """
    unit_price: Optional[StrictStr] = Field(None, alias="unitPrice", description="This field is unit price and it will always be positive whole number")
    unit_quantity: Optional[StrictStr] = Field(None, alias="unitQuantity", description="This field is unit quantity and it will always be positive whole number")
    __properties = ["unitPrice", "unitQuantity"]

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
    def from_json(cls, json_str: str) -> ItemDetails:
        """Create an instance of ItemDetails from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> ItemDetails:
        """Create an instance of ItemDetails from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return ItemDetails.parse_obj(obj)

        _obj = ItemDetails.parse_obj({
            "unit_price": obj.get("unitPrice"),
            "unit_quantity": obj.get("unitQuantity")
        })
        return _obj


