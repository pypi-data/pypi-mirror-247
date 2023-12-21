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

class ProductCustomerTagDTO(BaseModel):
    """
    ProductCustomerTagDTO
    """
    key: Optional[StrictStr] = Field(None, description="This object contains the user defined key-value pairs provided by the client. The maximum number of tags allowed is 15.  AU: Optional EU: Optional UK: Optional SG: Optional")
    value: Optional[StrictStr] = Field(None, description="This field accepts the value of the tag. The maximum value length limit is 256 characters.  AU: Optional EU: Optional UK: Optional SG: Optional")
    __properties = ["key", "value"]

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
    def from_json(cls, json_str: str) -> ProductCustomerTagDTO:
        """Create an instance of ProductCustomerTagDTO from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> ProductCustomerTagDTO:
        """Create an instance of ProductCustomerTagDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return ProductCustomerTagDTO.parse_obj(obj)

        _obj = ProductCustomerTagDTO.parse_obj({
            "key": obj.get("key"),
            "value": obj.get("value")
        })
        return _obj


