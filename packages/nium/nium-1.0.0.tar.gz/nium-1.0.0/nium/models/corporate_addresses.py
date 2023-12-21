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
from pydantic import BaseModel, Field
from nium.models.corporate_registered_address import CorporateRegisteredAddress

class CorporateAddresses(BaseModel):
    """
    CorporateAddresses
    """
    registered_address: Optional[CorporateRegisteredAddress] = Field(None, alias="registeredAddress")
    __properties = ["registeredAddress"]

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
    def from_json(cls, json_str: str) -> CorporateAddresses:
        """Create an instance of CorporateAddresses from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of registered_address
        if self.registered_address:
            _dict['registeredAddress'] = self.registered_address.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> CorporateAddresses:
        """Create an instance of CorporateAddresses from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return CorporateAddresses.parse_obj(obj)

        _obj = CorporateAddresses.parse_obj({
            "registered_address": CorporateRegisteredAddress.from_dict(obj.get("registeredAddress")) if obj.get("registeredAddress") is not None else None
        })
        return _obj


