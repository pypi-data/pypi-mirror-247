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

class CorporateAddress(BaseModel):
    """
    CorporateAddress
    """
    address_line1: Optional[StrictStr] = Field(None, alias="addressLine1", description="This field accepts the address line 1 of the stakeholder’s residential address.  AU: Required EU: Required UK: Required SG: Optional")
    address_line2: Optional[StrictStr] = Field(None, alias="addressLine2", description="This field accepts the address line 2 of the stakeholder’s residential address.  AU: Required EU: Optional UK: Optional SG: Optional")
    city: Optional[StrictStr] = Field(None, description="This field accepts the stakeholder’s residential city.  AU: Required EU: Required UK: Required SG: Optional")
    country: Optional[StrictStr] = Field(None, description="This field accepts the [2-letter ISO Alpha-2 country code](https://nium-documents.s3-eu-west-1.amazonaws.com/spend-documents/Country+Code.pdf) for the residential country of the stakeholder.  AU: Optional EU: Required UK: Required SG: Required")
    postcode: Optional[StrictStr] = Field(None, description="This field accepts the zip code or postal code of the stakeholder’s residential address.  AU: Optional EU: Required UK: Required SG: Required")
    state: Optional[StrictStr] = Field(None, description="This field accepts the state of the stakeholder’s residential address.  AU: Optional EU: Required UK: Required SG: Required")
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
    def from_json(cls, json_str: str) -> CorporateAddress:
        """Create an instance of CorporateAddress from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> CorporateAddress:
        """Create an instance of CorporateAddress from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return CorporateAddress.parse_obj(obj)

        _obj = CorporateAddress.parse_obj({
            "address_line1": obj.get("addressLine1"),
            "address_line2": obj.get("addressLine2"),
            "city": obj.get("city"),
            "country": obj.get("country"),
            "postcode": obj.get("postcode"),
            "state": obj.get("state")
        })
        return _obj


