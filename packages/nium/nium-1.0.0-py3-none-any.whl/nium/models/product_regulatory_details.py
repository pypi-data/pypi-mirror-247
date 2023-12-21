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


from typing import List, Optional
from pydantic import BaseModel, Field, StrictStr, conlist

class ProductRegulatoryDetails(BaseModel):
    """
    ProductRegulatoryDetails
    """
    regulated_trust_type: Optional[conlist(StrictStr)] = Field(None, alias="regulatedTrustType", description="This array accepts regulated trust type details. The possible values are as follows: ASIC - Registered Managed Investment Scheme MIS - Unregistered Managed Investment Scheme Regulated under a Commonwealth statutory regulator Government Superannuation Fund This field is required in case the region is AU and entity type [refer businessDetails.businessType] is a Regulated Trust.  AU: Optional EU: NA UK: NA SG: Optional")
    unregulated_trust_type: Optional[conlist(StrictStr)] = Field(None, alias="unregulatedTrustType", description="This array accepts unregulated trust type details. The possible values are as follows: Family Trust Charitable Trust Testamentary Trust Unit Trust Other Type This field is required in case the region is AU and entity type [refer businessDetails.businessType] is an Unregulated Trust  AU: Optional EU: NA UK: NA SG: NA")
    __properties = ["regulatedTrustType", "unregulatedTrustType"]

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
    def from_json(cls, json_str: str) -> ProductRegulatoryDetails:
        """Create an instance of ProductRegulatoryDetails from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> ProductRegulatoryDetails:
        """Create an instance of ProductRegulatoryDetails from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return ProductRegulatoryDetails.parse_obj(obj)

        _obj = ProductRegulatoryDetails.parse_obj({
            "regulated_trust_type": obj.get("regulatedTrustType"),
            "unregulated_trust_type": obj.get("unregulatedTrustType")
        })
        return _obj


