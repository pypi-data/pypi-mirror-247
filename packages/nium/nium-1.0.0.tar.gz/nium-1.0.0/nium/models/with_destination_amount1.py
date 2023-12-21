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


from typing import Optional, Union
from pydantic import BaseModel, Field, confloat, conint

class WithDestinationAmount1(BaseModel):
    """
    WithDestinationAmount1
    """
    destination_amount: Optional[Union[confloat(gt=0, strict=True), conint(gt=0, strict=True)]] = Field(None, alias="destinationAmount", description="The amount needed in the destination currency.")
    __properties = ["destinationAmount"]

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
    def from_json(cls, json_str: str) -> WithDestinationAmount1:
        """Create an instance of WithDestinationAmount1 from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> WithDestinationAmount1:
        """Create an instance of WithDestinationAmount1 from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return WithDestinationAmount1.parse_obj(obj)

        _obj = WithDestinationAmount1.parse_obj({
            "destination_amount": obj.get("destinationAmount")
        })
        return _obj


