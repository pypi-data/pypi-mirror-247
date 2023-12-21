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

class ProductTaxDetails(BaseModel):
    """
    ProductTaxDetails
    """
    country: Optional[StrictStr] = Field(None, description="This field accepts the 2-letter [ISO Alpha-2 country code](https://nium-documents.s3-eu-west-1.amazonaws.com/spend-documents/Country+Code.pdf) for the country of residence for tax purpose.  AU: NA EU: Required UK: NA SG: NA")
    tax_number: Optional[StrictStr] = Field(None, alias="taxNumber", description="This field accepts the tax ID number for each country of tax residence.  AU: NA EU: Required UK: NA SG: NA")
    __properties = ["country", "taxNumber"]

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
    def from_json(cls, json_str: str) -> ProductTaxDetails:
        """Create an instance of ProductTaxDetails from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> ProductTaxDetails:
        """Create an instance of ProductTaxDetails from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return ProductTaxDetails.parse_obj(obj)

        _obj = ProductTaxDetails.parse_obj({
            "country": obj.get("country"),
            "tax_number": obj.get("taxNumber")
        })
        return _obj


