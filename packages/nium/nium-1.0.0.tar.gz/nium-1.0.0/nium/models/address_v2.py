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

class AddressV2(BaseModel):
    """
    AddressV2
    """
    address_line1: Optional[StrictStr] = Field(None, alias="addressLine1", description="This field accepts the address line1 of the registered address for the new corporate entity to be onboarded.  AU: Required EU: Required UK: Required SG: Required")
    address_line2: Optional[StrictStr] = Field(None, alias="addressLine2", description="This field accepts the address line2 of the registered address for the new corporate entity to be onboarded.  AU: Required EU: Optional UK: Optional SG: Optional")
    city: Optional[StrictStr] = Field(None, description="This field contains the city of the stakeholder's address.")
    country: Optional[StrictStr] = Field(None, description="This field contains the country of the stakeholder's address.")
    post_code: Optional[StrictStr] = Field(None, alias="postCode", description="This field contains the zipCode of the stakeholder's address.")
    state: Optional[StrictStr] = Field(None, description="This field contains the state of the stakeholder's address.")
    __properties = ["addressLine1", "addressLine2", "city", "country", "postCode", "state"]

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
    def from_json(cls, json_str: str) -> AddressV2:
        """Create an instance of AddressV2 from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> AddressV2:
        """Create an instance of AddressV2 from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return AddressV2.parse_obj(obj)

        _obj = AddressV2.parse_obj({
            "address_line1": obj.get("addressLine1"),
            "address_line2": obj.get("addressLine2"),
            "city": obj.get("city"),
            "country": obj.get("country"),
            "post_code": obj.get("postCode"),
            "state": obj.get("state")
        })
        return _obj


