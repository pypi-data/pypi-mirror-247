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

class CustomerClientTagResponseDTO(BaseModel):
    """
    CustomerClientTagResponseDTO
    """
    key: Optional[StrictStr] = Field(None, description="This field contains the name of the tag.")
    message: Optional[StrictStr] = Field(None, description="This field contains the status message related to tag operation.")
    __properties = ["key", "message"]

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
    def from_json(cls, json_str: str) -> CustomerClientTagResponseDTO:
        """Create an instance of CustomerClientTagResponseDTO from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> CustomerClientTagResponseDTO:
        """Create an instance of CustomerClientTagResponseDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return CustomerClientTagResponseDTO.parse_obj(obj)

        _obj = CustomerClientTagResponseDTO.parse_obj({
            "key": obj.get("key"),
            "message": obj.get("message")
        })
        return _obj


