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

class AddressDTO(BaseModel):
    """
    AddressDTO
    """
    address_line1: Optional[StrictStr] = Field(None, alias="addressLine1", description="This field accepts the line 1 of the customer’s address. Maximum character limit: 100.")
    address_line2: Optional[StrictStr] = Field(None, alias="addressLine2", description="This field accepts the line 2 of the customer’s address. Maximum character limit: 100.")
    city: Optional[StrictStr] = Field(None, description="This field accepts the city of the customer’s address. Maximum character limit: 50.")
    country: Optional[StrictStr] = Field(None, description="This field accepts the 2-letter [ISO Alpha-2 country code](https://nium-documents.s3-eu-west-1.amazonaws.com/spend-documents/Country+Code.pdf) denoting the customer’s country.")
    postcode: Optional[StrictStr] = Field(None, description="This field accepts the postal code of the customer’s address. The acceptable special characters are: Hypen(-) Hash(#) Space( ) Minimum character limit: 3 Maximum character limit: 10 Example: CM-4165 65")
    state: Optional[StrictStr] = Field(None, description="This field accepts the state of the customer’s address")
    __properties = ["addressLine1", "addressLine2", "city", "country", "postcode", "state"]

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
    def from_json(cls, json_str: str) -> AddressDTO:
        """Create an instance of AddressDTO from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> AddressDTO:
        """Create an instance of AddressDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return AddressDTO.parse_obj(obj)

        _obj = AddressDTO.parse_obj({
            "address_line1": obj.get("addressLine1"),
            "address_line2": obj.get("addressLine2"),
            "city": obj.get("city"),
            "country": obj.get("country"),
            "postcode": obj.get("postcode"),
            "state": obj.get("state")
        })
        return _obj


