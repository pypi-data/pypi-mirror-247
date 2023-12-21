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

class CustomerTaxDetailDTO(BaseModel):
    """
    CustomerTaxDetailDTO
    """
    country_of_residence: Optional[StrictStr] = Field(None, alias="countryOfResidence", description="This field accepts the 2-letter [ISO Alpha-2 country code](https://nium-documents.s3-eu-west-1.amazonaws.com/spend-documents/Country+Code.pdf) denoting the country of residence, Note: This field is mandatory for EU and UK.")
    tax_id_number: Optional[StrictStr] = Field(None, alias="taxIdNumber", description="This field accepts the tax ID number of the customer, for example, \"FR123456\". Note: This field is mandatory for EU and UK.")
    __properties = ["countryOfResidence", "taxIdNumber"]

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
    def from_json(cls, json_str: str) -> CustomerTaxDetailDTO:
        """Create an instance of CustomerTaxDetailDTO from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> CustomerTaxDetailDTO:
        """Create an instance of CustomerTaxDetailDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return CustomerTaxDetailDTO.parse_obj(obj)

        _obj = CustomerTaxDetailDTO.parse_obj({
            "country_of_residence": obj.get("countryOfResidence"),
            "tax_id_number": obj.get("taxIdNumber")
        })
        return _obj


