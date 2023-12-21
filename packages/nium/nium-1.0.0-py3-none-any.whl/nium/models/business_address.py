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

class BusinessAddress(BaseModel):
    """
    BusinessAddress
    """
    address_line1: Optional[StrictStr] = Field(None, alias="addressLine1", description="This field accepts the address line1 of the business address for the new corporate entity to be onboarded. This field is required in case business address is being sent.  AU: Conditional EU: Conditional UK: Conditional SG: Conditional")
    address_line2: Optional[StrictStr] = Field(None, alias="addressLine2", description="This field accepts the address line 2 of the business address for the corporate entity.  AU: Conditional EU: Conditional UK: Conditional SG: Conditional")
    city: Optional[StrictStr] = Field(None, description="This field accepts the city of the business address for the new corporate entity to be onboarded. This field is required in case business address is being sent.  AU: Conditional EU: Conditional UK: Conditional SG: Conditional")
    country: Optional[StrictStr] = Field(None, description="This field accepts the the [2-letter ISO Alpha-2 country code](https://nium-documents.s3-eu-west-1.amazonaws.com/spend-documents/Country+Code.pdf) of the business address for the new corporate entity to be onboarded. This field is required in case business address is being sent.  AU: Conditional EU: Conditional UK: Conditional SG: Conditional")
    postcode: Optional[StrictStr] = Field(None, description="This field accepts the zip code or postal code of the business address for the new corporate entity to be onboarded. This field is required in case business address is being sent.  AU: Conditional EU: Conditional UK: Conditional SG: Conditional")
    state: Optional[StrictStr] = Field(None, description="This field accepts the state of the business address for the new corporate entity to be onboarded. This field is required in case business address is being sent.  AU: Conditional EU: Conditional UK: Conditional SG: Conditional")
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
    def from_json(cls, json_str: str) -> BusinessAddress:
        """Create an instance of BusinessAddress from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> BusinessAddress:
        """Create an instance of BusinessAddress from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return BusinessAddress.parse_obj(obj)

        _obj = BusinessAddress.parse_obj({
            "address_line1": obj.get("addressLine1"),
            "address_line2": obj.get("addressLine2"),
            "city": obj.get("city"),
            "country": obj.get("country"),
            "postcode": obj.get("postcode"),
            "state": obj.get("state")
        })
        return _obj


