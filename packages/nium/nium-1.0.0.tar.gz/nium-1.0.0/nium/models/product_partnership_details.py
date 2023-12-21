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

class ProductPartnershipDetails(BaseModel):
    """
    ProductPartnershipDetails
    """
    partner_country: Optional[StrictStr] = Field(None, alias="partnerCountry", description="This field accepts the country where partnership was established.  AU: Optional EU: NA UK: NA SG: Optional")
    partner_name: Optional[StrictStr] = Field(None, alias="partnerName", description="This field accepts the partner name.  AU: Optional EU: NA UK: NA SG: Optional")
    partner_state: Optional[StrictStr] = Field(None, alias="partnerState", description="This field accepts the state where partnership was established.  AU: Optional EU: NA UK: NA SG: Optional")
    __properties = ["partnerCountry", "partnerName", "partnerState"]

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
    def from_json(cls, json_str: str) -> ProductPartnershipDetails:
        """Create an instance of ProductPartnershipDetails from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> ProductPartnershipDetails:
        """Create an instance of ProductPartnershipDetails from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return ProductPartnershipDetails.parse_obj(obj)

        _obj = ProductPartnershipDetails.parse_obj({
            "partner_country": obj.get("partnerCountry"),
            "partner_name": obj.get("partnerName"),
            "partner_state": obj.get("partnerState")
        })
        return _obj


